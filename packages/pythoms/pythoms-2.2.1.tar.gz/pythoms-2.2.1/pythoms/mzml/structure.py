"""
Data structure for working with mzML files
"""
import gzip
import sys
import warnings
from random import random
from typing import Generator, List, MutableMapping
from xml.etree import ElementTree
from functools import wraps
from collections.abc import MutableSequence

import numpy as np
from tqdm import tqdm

from .logging import logger
from ..tome import resolution, locate_in_list, slice_array
from ..spectrum import Spectrum
from .psims import CVParameterSet
from .parsing import fps, scan_properties, branch_attributes, spectrum_array, get_element_units, _find_ele, _findall_ele
from .io import file_present, pw_convert, fix_extension


class BoundsError(Warning):
    """A warning class to handle bounds errors when integrating (used only by PyRSIR)"""

    def __init__(self):
        self.warned = {}

    def printwarns(self):
        """prints the number of warnings if merited"""
        if len(self.warned) > 0:
            logger.warning(
                'The following peaks exceeded the bounds of the spectrum n number of times:\n'
                f'{", ".join([f"{name}: {self.warned[name]}" for name in self.warned])}'
            )

    def warn(self, name, intstart, intend, mzstart, mzend):
        """warns the user if there was a mismatch"""
        if name not in self.warned:
            logger.warning(
                f'The peak "{name}" ({intstart}-{intend}) is outside of the bounds of the spectrum being summed '
                f'm/z {mzstart:.1f}-{mzend:.1f}\n'
            )
            self.warned[name] = 1
        else:
            self.warned[name] += 1


class Trace(MutableSequence):
    def __init__(self,
                 *incoming_values: float,
                 center_bin: bool = False,
                 ):
        """
        A data class for managing binned values of a trace. The class stores raw data and retains binned traces
        after they are generated (prevents re-binning data when the data is used in multiple locations).

        :param incoming_values: values to add on instantiation
        :param center_bin: whether to center the bin value
        """
        self._raw_data: List[float] = []
        self._binned_data: MutableMapping[int, List[float]] = {}
        self.center_bin: bool = center_bin
        # self._bin_valid: bool = False  # todo enable tracking of bin validity (once new value added, prev bins invalid)

        for value in incoming_values:
            self.append(value)

    def __getitem__(self, item) -> float:
        return self._raw_data[item]

    def __setitem__(self, key, value):
        self._raw_data[key] = value

    def __delitem__(self, key):
        del self._raw_data[key]

    def __len__(self):
        return len(self._raw_data)

    def __copy__(self):
        return self.__class__(
            *self._raw_data,
            center_bin=self.center_bin,
        )

    @property
    def raw_data(self) -> List[float]:
        """raw data list (unbinned)"""
        return self._raw_data

    def insert(self, index: int, val: float) -> None:
        """
        Inserts a value at the position specified

        :param index: index
        :param val: value
        """
        self._raw_data.append(val)

    def get_binned_data(self, bin_num: int) -> List[float]:
        """
        Bins the data into bins of the size specified. If the data has already been binned to that level, returns the
        previously binned data.

        :param bin_num: bin number to use
        :return: list of binned values
        """
        # if previously binned, return
        if bin_num in self._binned_data:
            return self._binned_data[bin_num]
        # bin data
        out = self.bin_trace(
            bin_num,
            self.raw_data,
            bin_denom=bin_num if self.center_bin else 1,
        )
        # store data for later retrieval
        self._binned_data[bin_num] = out
        return out

    @staticmethod
    def bin_trace(bin_num: int, target_list: List[float], bin_denom=1):
        """
        Bins a list of values into bins of size *bin_num*.

        :param bin_num: Number of values to bin together. e.g. ``n = 4`` would bin the first four values into a single
            value, then the next 4, etc.
        :param target_list: List of values to bin.
        :param bin_denom: Bin denominator. The calculated bin values will be divided by this value. e.g. if ``n = v`` the
            output values will be an average of each bin.
        :return: binned list

        **Notes**

        - If the size of the list is not divisible by `bin_num`, the final bin will not be included in the output list.
        (The last values will be discarded.)

        """
        out = []
        delta = 0
        ttemp = 0
        for ind, val in enumerate(target_list):
            delta += 1
            ttemp += val  # add current value to growing sum
            if delta == bin_num:  # critical number is reached
                out.append(ttemp / float(bin_denom))  # append sum to list
                delta = 0  # reset critical count and sum
                ttemp = 0
        return out


class mzML(object):
    def __init__(self,
                 filename: str,
                 verbose: bool = True,
                 precision: int = 64,
                 compression: bool = True,
                 gzip_file: bool = True,
                 obo: str = None,
                 ftt: bool = False,
                 **kwargs
                 ):
        """
        A class for loading and extracting data from an mzML file.

        :param str filename: The name of the mzML or mass spectrometric data file. Accepted file types are listed below,
            and this script can automatically convert some proprietary file types to mzML by calling ProteoWizard
            (see notes).
        :param bool verbose: Chatty enable or disable. It can be useful to enable this when processing large files or long
            acquisitions, as many of the methods have progress reporters.
        :param int precision: The floating point precision to use if converting to mzML. Default 64 (although this
            appears to have a minimal effect in the experience of the author). This can be set to 32 to decrease mzML
            file sizes.
        :param bool compression: Whether or not to compress the mzML files when converting. This can decrease file
            sizes at a slight cost in processing time.
        :param bool gzip: Whether or not to gzip the mzML files when converting. This substantially decreases file
            sizes (mass spectrometric data compresses very well when gzipped). This will slightly increase processing
            time.
        :param str obo: A specific path or URL to an *.obo file defining the accession keys used in mzML files. If this
            is not specified, the default accession URL will be used to download the required obo file. This should not
            be necessary normally, as most of the commonly encountered accession keys are hard-coded into this
            script. The script will raise an error if it encounters an undefined accession key.
        :param bool ftt:  Whether to run the function_timetic() method on initialization. This is useful if you require
            access to the total ion current and time lists for each function in the mzML file. This does increase file
            load times quite significantly (~6x slower).

        **Notes**

        An mzML file is a data format for mass spectrometric data which can be parsed by python (avoiding the pitfalls
        associated with the proprietary files usually generated by the mass spectrometers themselves). The mzML file
        structures are expected to conform to those outlined in the HUPO Proteomics Standards Working Group. More
        information can be found at https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo

        If you wish to use the format conversion functionality of this script, you will need to download and install
        ProteoWizard, which can be found at http://proteowizard.sourceforge.net/

        """
        # store keyword settings
        self.verbose = verbose
        self.precision = precision
        self.compression = compression
        self.gzip_file = gzip_file
        self.obo = obo

        self.filename = self.check_for_file(filename)

        logger.info(f'Loading {self.filename} into memory')
        if self.filename.lower().endswith('.mzml.gz'):  # if mzml is gzipped
            handle = gzip.open(self.filename)  # unzip the file
        else:
            handle = self.filename
        try:
            self.tree = ElementTree.parse(handle)  # full mzML file
            self.root = self.tree.getroot()
        except:
            raise IOError(
                'The mzML file "%s" could not be loaded. The file is either unsupported, corrupt, or incomplete.' % self.filename)

        try:  # number of spectra
            nscans = _find_ele('mzML', 'run', 'spectrumList', parent=self.root)
            self.nscans = int(nscans.attrib['count'])
        except IndexError:  # no spectra
            self.nscans = 0
        try:
            ncrhoms = _find_ele('mzML', 'run', 'chromatogramList', parent=self.root)
            self.nchroms = int(ncrhoms.attrib['count'])
        except IndexError:
            self.nchroms = 0

        self.functions = {}
        for spectrum in self.spectra_elements:
            try:
                # try to retrieve function, process, and scan from attributes
                func, proc, scan = fps(spectrum)  # extract each value and convert to integer
            except ValueError:
                # if undefined, assume only one function
                func = 1
            if func not in self.functions:  # if function is not defined yet
                p = CVParameterSet.create_from_branch(spectrum)  # pull spectrum's cvparameters
                self.functions[func] = {
                    'sr': [int(spectrum.attrib.get('index')), None],  # the scan index range that the function spans
                    'nscans': 1,  # number of scans
                }
                self.functions[func].update(scan_properties(p))  # update with scan properties
            else:
                self.functions[func]['sr'][1] = int(
                    spectrum.attrib.get('index'))  # otherwise set the scan index range to the current index
                self.functions[func]['nscans'] += 1
        try:
            p = CVParameterSet.create_from_branch(spectrum)  # pull properties of final spectrum
            self.duration = p['MS:1000016'].value  # final start scan time
        except (KeyError, UnboundLocalError):  # if there are no spectra, set to None
            # todo figure out a catch to retrieve time from other sources (e.g. TIC)
            self.duration = None

        self._BE = BoundsError()  # load warning instance for integration
        self._ftt_extracted = False
        if ftt is True:
            self.extract_function_time_tic()

    def __str__(self):
        """The string that is returned when printed"""
        return f'{self.__class__.__name__} {self.nscans} spectra, {self.nchroms} chromatograms'

    def __repr__(self):
        """The representation that is returned"""
        return "%s('%s')" % (self.__class__.__name__, self.filename)

    def __len__(self):
        return self.nscans

    def __getitem__(self, ind):
        """retrieves a scan or summed scans"""
        if isinstance(ind, slice):  # if getitem is trying to slice
            """
            returns the summed scans with the supplied indicies
            slice will assume that the intended function is 1
            """
            if ind.start is None:  # no start
                start = 0
            else:
                start = ind.start
            if ind.stop is None:  # no stop
                stop = self.functions[1]['sr'][1]
            else:
                stop = ind.stop
            return self.sum_scans(start, stop, mute=True)

        elif type(ind) is int:  # scan index number
            """will return the spectrum of the scan index provided"""
            if ind < 0 or ind > self.nscans:
                raise IndexError("The scan index number #%d is outside of the mzML's scan index range (0-%d)" % (
                ind, self.nscans - 1))
            for spectrum in self.spectra_elements:
                attr = branch_attributes(spectrum)
                if attr['index'] == ind:
                    return spectrum_array(spectrum)

        elif type(ind) is float:  # timepoint in function 1
            """float will assume the intended function was 1"""
            if ind < 0 or ind > self.duration:
                raise ValueError(
                    "The supplied time %.3f is outside of this file's time range (0 - %.3f)" % (ind, self.duration))
            ind = self.scan_index(ind)
            for spectrum in self.spectra_elements:
                attr = branch_attributes(spectrum)
                if attr['index'] == ind:
                    return spectrum_array(spectrum)

    @property
    def spectra_elements(self) -> Generator[ElementTree.Element, None, None]:
        """generator of spectra elements"""
        for element in _findall_ele('mzML', 'run', 'spectrumList', 'spectrum', parent=self.root):
            yield element

    @property
    def chromatogram_elements(self) -> Generator[ElementTree.Element, None, None]:
        """generator of chromatogram elements"""
        for element in _findall_ele('mzML', 'run', 'chromatogramList', 'chromatogram', parent=self.root):
            yield element

    @property
    def _mute_tqdm(self) -> bool:
        """whether to mute tqdm"""
        return not self.verbose

    def foreachchrom(self, fn):
        """
        a decorator function that will apply the supplied function to every chromatogram in the mzml file
        the supplied function will be handed the chromatogram XML object as the first argument
        the decorated function will return a list of outputs of the supplied function where each index corresponds to a scan

        e.g.::
            loaded = mzML(filename)

            @loaded.foreachchrom
            def do_this(chrom):
                # extract the attributes using the mzML.attributes() method
                attr = loaded.attributes(chrom)
                return attr['id'] # return the name of the chromatogram

            do_this()

        """

        def foreachchrom(*args, **kwargs):
            """decorates the supplied function to run for every scan"""
            out = []
            msg = f'applying function to chromatogram'
            for chromatogram in tqdm(self.chromatogram_elements, desc=msg, disable=self._mute_tqdm):
                out.append(fn(chromatogram, *args, **kwargs))
            return out

        return foreachchrom

    def foreachscan(self, fn):
        """
        a decorator function that will apply the supplied function to every spectrum in the mzml file
        the supplied function will be handed the spectrum XML object as the first argument
        the decorated function will return a list of outputs of the supplied function where each index corresponds to a scan

        e.g.::

            loaded = mzML(filename)

            @loaded.foreachscan
            def do_this(scan):
                p = loaded.cvparam(scan) # pull spectrum's cvparameters
                sst = p['MS:1000016'] # start scan time
                x,y = loaded.extract_spectrum(scan,False) # extract the x,y spectrum
                # return the start scan time, x list, and y list
                return sst,x,y

            do_this() # do it
        """

        def foreachscan(*args, **kwargs):
            """decorates the supplied function to run for every scan"""
            out = []
            msg = 'applying function to spectrum'
            for spectrum in tqdm(self.spectra_elements, desc=msg, disable=self._mute_tqdm):
                out.append(fn(spectrum, *args, **kwargs))
            return out

        return foreachscan

    def associate_to_function(self, affin=None, level=None, dct=None):
        """
        Associates a given species to the appropriate function number
        in the mzML data file.

        **Parameters**

        affin: '+', '-', or 'UV'
            The affinity of the species. i.e. to positive mode,
            negative mode, or UV-Vis spectra respectively.

        level: *integer* or None
            If the species is found in an MS/MS function,
            the MS^n level can be specified here.

        dct: *dictionary*
            If details are known about the species' affinity,
            they can be provided in dictionary format.
            Specifically, this function looks for the keys:
            'function', 'affin', and 'level'.


        **Returns**

        function number: *integer*
            Returns the appropriate function number in which
            the given species should be found.


        **Notes**

        If nothing is provided to this method, it will return
        the integer 1 (assuming that the species will be found
        in the first function).

        """
        if dct is not None:  # if function was handed a dictionary
            if 'function' in dct:
                return dct['function']
            if 'affin' in dct:
                affin = dct['affin']
            if 'level' in dct:
                level = dct['level']

        if affin is None and level in [None, 1]:
            return min(self.functions.keys())  # assume first function

        elif affin == 'UV':  # if UV-Vis affinity
            for fn in self.functions:  # determine which function is UV-Vis
                if self.functions[fn]['acc'] == 'MS:1000804':
                    return fn
            raise ValueError('There is no electromagnetic radiation spectrum function in this mzML file')

        elif affin in ['+', '-']:  # if affinity to mass spectrum
            levelcount = 0  # counter for number of matches to this affinity and level
            for fn in self.functions:
                if self.functions[fn]['type'] == 'MS':  # if fn is ms
                    if self.functions[fn]['mode'] == affin:  # if mode mathes
                        # if there is no level specified, assume 1
                        if level is None and self.functions[fn]['level'] == 1:
                            fnout = fn
                            levelcount += 1
                        elif self.functions[fn]['level'] == level:  # if level matches
                            fnout = fn
                            levelcount += 1
            if levelcount > 1:
                raise ValueError(
                    f"There affinity specification of mode: {affin}, level: '{level}' matches more than one function "
                    f"in the mzML file. \nTo process this species, be more specific in your level specification or "
                    f"assign it to a specific function number by adding a 'function' key to its dictionary.")
            return fnout
        else:  # if some other affinity
            raise ValueError('The specified affinity "%s" is not supported.' % affin)

    def auto_resolution(self, n=10, function=None, npeaks=4):
        """
        Attempts to automatically determine the resolution of the spectrometer
        that the provided mzML data file was recorded on.
        The method will find n random samples of the entire spectrum and
        calculate the resolution of each of those samples and return the
        average resolution.

        :param int n: The number of psuedo-random samples of the spectrum to determine
            the resolution of. Default 10.
        :param int function: The mzML function number to calculate the resolution of. Default 1.
        :param int npeaks: number of peaks to to try to find
        :return: Estimated resolution of the spectrum
        :rtype: float
        """
        def findsomepeaks(y):
            """roughly locates 4 peaks by maximum values in the spectrum and returns their index"""
            split = int(len(y) / npeaks)
            start = 0
            end = start + split
            splity = []
            for i in range(npeaks):
                splity.append(np.asarray(y[start:end]))
                start += split
                end += split
            out = []
            for ind, section in enumerate(splity):
                maxy = max(section)
                if maxy == max(section[1:-1]):  # if max is not at the edge of the spectrum
                    out.append(np.where(section == maxy)[0][0] + split * ind)
            return out

        if function is None:  # if no function is provided, use first
            function = self.associate_to_function()
        if self.functions[function]['type'] != 'MS':
            raise ValueError(
                'The auto_resolution function only operates on mass spectrum functions. '
                'Type of specified function %d: %s' % (function, self.functions[function]['type']))
        ranges = []  # list of scan intervals

        if self.functions[function]['nscans'] <= 20:  # if the number of scans is less than 20
            ranges = [[1, self.functions[function]['nscans']]]
        else:
            while len(ranges) < n:  # generate 10 pseudo-random intervals to sample
                ran = int(random() * self.functions[function]['nscans']) + self.functions[function]['sr'][0]
                if ran - 10 >= self.functions[function]['sr'][0] and ran + 10 <= self.functions[function]['sr'][1]:
                    ranges.append([ran - 10, ran + 10])
        summed = []
        msg = 'Estimating resolution of the instrument'
        for ind, rng in enumerate(tqdm(ranges, desc=msg, disable=self._mute_tqdm)):
            summed.append(  # sum those scans and append output
                self.sum_scans(
                    rng[0], rng[1],
                    function,
                    2,
                    mute=True
                )
            )
        res = []
        for spec in summed:  # calculate resolution for each scan range
            inds = findsomepeaks(spec[1])  # find some peaks
            for ind in inds:  # for each of those peaks
                res.append(resolution(spec[0], spec[1], ind, threshold=10))
        res = [y for y in res if y is not None]  # removes None values (below S/N)
        return sum(res) / len(res)  # return average

    def check_for_file(self, fn):
        """checks for the mzML file in the working directory and converts it if necessary"""
        # cast path-like to string to enable extension check
        if type(fn) is not str:
            fn = str(fn)

        valid = [  # supported extensions
            '.raw',
            '.mzml.gz',
            '.mzml',
        ]
        if fn.lower().endswith('.raw') is True:  # extension is raw
            if file_present(fn[:-4] + '.mzML.gz') is True:  # if corresponding gzipped mzml is present
                return fn[:-4] + '.mzML.gz'
            if file_present(fn[:-4] + '.mzML') is True:  # if corresponding mzml is present
                return fn[:-4] + '.mzML'
            # otherwise convert and return mzml
            return pw_convert(fn, self.precision, self.compression, self.gzip_file, verbose=self.verbose)
        elif file_present(fn) is True:  # if the specified file is present
            for exten in valid:  # checks for supported extensions
                if fn.lower().endswith(exten) is True:
                    return fn
            # otherwise asks user whether to continue
            if input(
                    'The extension of the supplied filename "%s" is unexpected and may not be supported.\n'
                    'Do you wish to proceed with file loading? [Y/N] ' % fn).lower() in ['y', 'yes']:
                return fn
            else:
                sys.exit('The user cancelled mzML loading.')
        else:
            fn = fix_extension(fn)  # try to fix extension
            if fn.lower().endswith('.raw') is True:  # convert if only raw file is found
                return pw_convert(fn, self.precision, self.compression, self.gzip_file, verbose=self.verbose)
            return fn

    def _ensure_ftt_extracted(fn):
        """
        checks whether function, time, and TIC lists have been extracted and extracts them if not
        (runtime method of ensuring the data is there)
        """
        @wraps(fn)
        def decorated(self: 'mzML', *args, **kwargs):
            if self._ftt_extracted is False:
                self.extract_function_time_tic()
            return fn(self, *args, **kwargs)
        return decorated

    def extract_function_time_tic(self):
        """
        extracts timepoints and tic lists for each function
        this function is separate from mzml contents because it would increase load times significantly (~6x)
        """
        # todo see if there's a way to sneakily do this the first time the user iterates through spectra
        # todo come up with a data class to manage function metadata
        msg = 'extracting timepoints and total ion current values'
        for function in self.functions:  # add timepoint and tic lists
            self.functions[function]['timepoints'] = Trace(center_bin=True)  # list for timepoints
            self.functions[function]['tic'] = Trace()  # list for total ion current values
            if 'level' in self.functions[function] and self.functions[function]['level'] > 1:
                self.functions[function]['ce'] = Trace()  # list for collision energies
        for spectrum in tqdm(self.spectra_elements, desc=msg, disable=self._mute_tqdm, total=self.nscans):
            # attr = branch_attributes(spectrum)
            function, proc, scan = fps(spectrum)  # determine function, process, and scan numbers
            p = CVParameterSet.create_from_branch(spectrum)  # pull spectrum's cvparameters
            self.functions[function]['timepoints'].append(p['MS:1000016'].value)  # start scan time
            self.functions[function]['tic'].append(p['MS:1000285'].value)  # total ion current
            if 'MS:1000045' in p:
                self.functions[function]['ce'].append(p['MS:1000045'].value)  # collision energy
        self._ftt_extracted = True

    @_ensure_ftt_extracted
    def get_timepoints_of_function(self, function: int) -> Trace:
        """
        Retrieves the timepoints of the specified function

        :param function: function number
        :return: Trace of data
        """
        return self.functions[function]['timepoints']

    @_ensure_ftt_extracted
    def get_tic_of_function(self, function: int) -> Trace:
        """
        Retrieves the total ion current (TIC) of the specified function

        :param function: function number
        :return: Trace of data
        """
        return self.functions[function]['tic']

    def integrate(self, name, start, end, x, y):
        """
        Integrates y values given x bounds in a paired set of lists (e.g. a m/z list and an intensity list)

        name: name of the peak being integrated (only used for warning purposes)
        start: float
            start x value
        end: float or None
            end x value
            None will return the nearest value to the provided start value
        x: list of x values
        y: list of y values (paired with x)

        returns: integral
        """
        if start > max(x) or start < min(x):  # check that start is within the m/z bounds
            self._BE.warn(name, start, end, min(x), max(x))
        if end is None:  # if only a start value is supplied, return closest to that value
            try:  # try to find the value in the list
                return y[locate_in_list(x, start)]
            except TypeError:  # if the value is not in the list, return 0
                return 0
        if end > max(x):  # check that end is within the m/z bounds
            self._BE.warn(name, start, end, min(x), max(x))
        else:
            l = locate_in_list(x, start, 'greater')
            r = locate_in_list(x, end, 'lesser')
            if l <= r:
                return sum(y[l:r])
            else:  # catch for if there are no values in the bounds
                return 0

    def pull_chromatograms(self):
        """
        Pulls mzML chromatograms

        returns:
        dictionary = {'chromatogram 1 id', 'chromatogram 2 id', ...}
        dictionary['chromatogram 1 id'] = {
        'x': list of x values
        'y': list of y values (paired with x)
        'xunit': unit of the x values
        'yunit': unit of the y values
        }
        """
        msg = 'extracting chromatogram'
        chroms = {}  # dictionary of chromatograms
        for chromatogram in tqdm(self.chromatogram_elements, desc=msg, disable=self._mute_tqdm):
            attr = branch_attributes(chromatogram)  # pull attributes
            chrom_array = spectrum_array(chromatogram)
            xunit, yunit = get_element_units(chromatogram)
            chroms[attr['id']] = {
                'x': chrom_array[0],
                'y': chrom_array[1],
                'xunit': xunit,
                'yunit': yunit,
            }
        return chroms

    @_ensure_ftt_extracted
    def pull_species_data(self, sp, sumspec=False):
        """
        Extracts integrated data at every timepoint for all species specified in the sp dictionary
        This function is intended to by called by PyRSIR.py

        sp: dictionary
        sp = {species1, species2, ...} //one key for every species to track
        sp[species] = {
        'bounds':[species x start, species x end], //start and end x values to integrate between
        'affin':['+' or '-' or 'UV'}, //which spectrum to look for this species in
        'level':integer, //if applicable, the MSn level (optional, but adds specificity)
        'function':integer, //the specific function in which to find this species (optional; overrides affin and level)
        }

        sumspec: bool
            toggles summing of all spectra together (creates an additional output item)
            also sums the spectra of mass spectrum species to generate an isotope pattern used by the bounds

        output:
            filled dictionary, each subkey will have:
            'raw': list of raw integrated values dictacted by the bounds
            'function': the function that the species was associated with

            if sumspec is true, will also output a dictionary of Spectrum objects
            the keys of this dictionary are the function numbers

        explicitly interprets full scan mass spectra and UV species
        """
        warnings.warn(
            'This is a legacy method used with the older PyRSIR, please use the new RSIRTarget and and PyRSIR class.',
            DeprecationWarning,
            stacklevel=2,
        )
        if sumspec is True:
            spec = {}
            for function in self.functions:  # create spectrum objects for all MS species
                if self.functions[function]['type'] == 'MS':
                    spec[function] = Spectrum(3)
        for species in sp:  # look for and assign function affinity
            sp[species]['function'] = self.associate_to_function(
                dct=sp[species])  # associate each species in the spectrum with a function
            if 'raw' not in sp[species]:  # look for empty raw list
                sp[species]['raw'] = []

        msg = 'extracting species data from spectrum'
        for spectrum in tqdm(self.spectra_elements, desc=msg, disable=self._mute_tqdm, total=self.nscans):
            function, proc, scan = fps(spectrum)  # pull function, process, and scan numbers
            # attr = branch_attributes(spectrum)  # get attributes
            spec_array = spectrum_array(spectrum)  # generate spectrum
            if sumspec is True and function == 1:
                spec[function].add_spectrum(spec_array[0], spec_array[1])
            for key in sp:  # integrate each peak
                if sp[key]['function'] == function:  # if species is related to this function
                    intensity = slice_array(
                        spec_array[1],
                        spec_array[0],
                        *sp[key]['bounds'],
                    )[1].sum()
                    # if UV trace, integrate and divide by 1 million bring it into au
                    if self.functions[function]['type'] == 'UV':
                        intensity /= 1000000.
                    sp[key]['raw'].append(intensity)

        self._BE.printwarns()  # print bounds warnings (if any)
        if sumspec is True:
            return sp, spec
        return sp, None

    @property
    def scans(self):
        """a generator for scans in """
        return

    @_ensure_ftt_extracted
    def retrieve_scans(self, start=None, end=None, mzstart=None, mzend=None, function=None, mute=False, outside=False):
        """
        Retrieves the specified scans or time range from the specified function

        start: integer or float
            the point to start retrieving scans
            if integer, this will be a start scan number
            if float, this will be the start time
        end: (optional) integer or float
            the end point to stop retrieving scans
            same options as start
        mzstart: (optional) integer or float
            left m/z bound
        mzend: (optional) integer or float
            right m/z bound
        fn: integer
            the function to pull scans from (default 1)
        mute: bool
            overrides the verbose setting of the mzml instance
        outside: bool
            Whether to include the next point outside of the specified m/z bounds.
            This is useful for line continuity if the spectrum is to be used for
            rendering images.

        returns a list with each index corresponding to a scan, with two sublists for x and y data
        """
        if function is None:  # if not specified, retrieve first function
            function = self.associate_to_function()
        # find spectrum indicies to extract between
        if function not in self.functions:
            raise ValueError('The function "%d" is not in this mzml file.' % function)
        start = self.scan_index(start, function, bias='greater')
        end = self.scan_index(end, function, bias='lesser')
        msg = 'retrieving scans'
        out = []
        for spectrum in tqdm(self.spectra_elements, desc=msg, disable=self._mute_tqdm, total=end - start):
            attr = branch_attributes(spectrum)
            # func,proc,scan = self.fps(spectrum) # determine function, process, and scan numbers
            # p = CVParameterSet.create_from_branch(spectrum)
            if attr['index'] > end:
                break
            if start <= attr['index'] <= end:  # within the index bounds
                spec_array = spectrum_array(spectrum)
                if mzstart is not None or mzend is not None:
                    spec_array = slice_array(
                        spec_array[1],
                        spec_array[0],
                        mzstart or spec_array[0].min(),
                        mzend or spec_array[0].max(),
                        outside=outside,
                    )
                out.append(spec_array)
        if len(out) == 1:  # if only one scan, return that scan
            return out[0]
        return out

    @_ensure_ftt_extracted
    def scan_index(self, scan=None, function=1, bias='lesser'):
        """
        Determines the index for a scan or timepoint in a given function

        :param int, float scan: The scan number (int) or time point (float) to find.
        :param int function: The mzml function to look in
        :param str bias: Bias of index finding (options dictacted by locate_in_list() )
        :return: scan index
        :rtype: int
        """
        if function not in self.functions:
            raise KeyError('The function %d is not in this mzML file.' % function)
        if scan is None:  # if no scan number is specified
            if bias == 'greater':  # used for start point
                return self.functions[function]['sr'][0]
            if bias == 'lesser':  # used for end point
                return self.functions[function]['sr'][1]
        if type(scan) is float:  # timepoint
            # return located index plus start of the scan range
            return locate_in_list(self.functions[function]['timepoints'], scan, bias=bias) + self.functions[function]['sr'][0]
        elif type(scan) is int:  # scan number
            if scan < 1:
                raise ValueError('The scan number must be greater or equal to 1 (specified: %d)' % scan)
            if scan > self.functions[function]['nscans']:
                raise ValueError(f'The scan number {scan} exceeds the number of scans in function {function} '
                                 f'({self.functions[function]["nscans"]})')
            # return scan minus 1 (to shift into index domain) plus the start location index
            return scan - 1 + self.functions[function]['sr'][0]
        else:
            raise ValueError(f'An unexpected scan type was handed to the scan_index function ("{scan}", '
                             f'type: {type(scan)})')

    def sum_scans(self,
                  start=None,
                  end=None,
                  function=None,
                  dec=3,
                  mute=False
                  ):
        """
        Sums the specified scans together. If the scan range moves into another function, an error is raised.
        This method has a lower memory overhead than retrieve_scans().

        :param float, int start: start point to begin summing. ``int`` is interpreted as a scan number, ``float`` is
            interpreted as a time point in the acquisition.
        :param float, int end: end point to finish summing. Parameters are the same as with start.
        :param int function: mzML function to sum. If this is not provided, the first function will be used.
        :param int dec: number of decimal places to track in the spectrum (lower values lower memory overhead).
        :param bool mute: override chatty mode of mzML object
        :return: summed spectrum in the format ``[[m/z values], [intensity values]]``
        :rtype: list
        """

        # if no function is specified, use the first function
        if function is None:
            if len(self.functions) == 0:
                raise IndexError('The sum_scans method requires functions to be associated with the mzML file. There '
                                 'are none associated with this file. ')
            function = min(self.functions.keys())
        elif function not in self.functions:  # if fn is not defined
            raise KeyError(f'The function {function} is not defined in the mzML object. Available options: '
                           f'{", ".join([str(key) for key in self.functions.keys()])}')
        if self.functions[function]['type'] != 'MS':
            raise ValueError(f'The sum_scans function does not have the functionality to sum non-mass spec scans.'
                             f'The specified function {function} is of type {self.functions[function]["type"]}')
        start = self.scan_index(start, function, 'greater')
        end = self.scan_index(end, function, 'lesser')

        spec = Spectrum(  # create Spectrum object
            dec,
            start=self.functions[function]['window'][0],
            end=self.functions[function]['window'][1]
        )

        msg = 'combining spectra'
        for spectrum in tqdm(self.spectra_elements, desc=msg, disable=self._mute_tqdm or mute, total=end - start):
            attr = branch_attributes(spectrum)  # get attributes
            if attr['index'] > end:
                break
            if start <= attr['index'] <= end:  # if within the specified bounds
                x, y = spectrum_array(spectrum)  # pull spectrum
                spec.add_spectrum(x, y)  # add spectrum to Spectrum object
        out = spec.trim()
        return out

    # set as static method for decorator to work
    _ensure_ftt_extracted = staticmethod(_ensure_ftt_extracted)
