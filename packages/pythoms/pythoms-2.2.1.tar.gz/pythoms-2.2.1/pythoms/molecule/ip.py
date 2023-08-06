import copy
import os
import pickle
from datetime import datetime

import numpy as np
import pylab as pl
from scipy import stats

from .parsing import interpret_charge
from .util import standard_deviation
from .mass import abbreviations, check_in_mass_dict
from .algorithms import isotope_pattern_combinatoric, isotope_pattern_multiplicative, isotope_pattern_hybrid, \
    isotope_pattern_isospec, bar_isotope_pattern, gaussian_isotope_pattern, VALID_IPMETHODS, VALID_DROPMETHODS
from .logging import logger
from .base import Molecule
from .settings import VERBOSE


def pattern_molecular_weight(mzs: list, intensities: list, charge: int = 1):
    """
    Calculates the molecular weight given by an isotope pattern.

    :param mzs: m/z (x) values for pattern
    :param intensities: intensity (y) values for the pattern
    :param charge: charge for the molecule
    :return: molecular weight
    :rtype: float
    """
    return sum([  # sum
        mz * intensity * charge  # of the product of the m/z, intensity, and charge
        for mz, intensity in zip(mzs, intensities)  # for all the values
    ]) / sum(intensities)  # divided by the sum of the intensities


def molecular_weight_error(calculated: float, expected: float):
    """
    Calculate the error between a calculated and expected molecular weight. This method may be used as a validation
    tool for calculated isotope patterns.

    :param calculated: calculated molecular weight (derived from an isotope pattern)
    :param expected: expected (true) molecular weight (derived from the molecular weights of the constituent elements)
    :return: Calculated error. Typically a difference of 3 parts per million (3*10^-6) is deemed an acceptable
        error.
    :rtype: float
    """
    return (calculated - expected) / expected


class IPMolecule(Molecule):
    _ipmethod = None
    _gausip = None  # gaussian isotope pattern storage
    _dropmethod = None

    def __init__(self,
                 string: (str, dict),
                 charge=1,
                 consolidate=3,
                 criticalerror=3 * 10 ** -6,
                 decpl=7,
                 dropmethod=None,
                 emptyspec=True,
                 groupmethod='weighted',
                 ipmethod='isospec',
                 keepall=False,
                 npeaks=5000,
                 resolution=5000,
                 threshold=0.01,
                 save=False,
                 verbose=VERBOSE,
                 precalculated=None,
                 mass_key: str = 'nist_mass',
                 ):
        """
        A class with many mass-spectrometric properties such as estimated exact masses, isotope patterns, error
        estimators, and basic plotting tools.

        :param str string: the molecule name to interpret. See Molecule documentation for more details
        :param int, str charge: the charge of the molecule (for mass spectrometric applications).
            This will affect any properties related to the mass to charge
            ratio. If the charge is specified in the input molecular formula, this will be
            overridden.

        :param int, float resolution: The resolution of the instrument to simulate when generating the gaussian isotope
            pattern. This also affects the bounds attribute.

        :param int consolidate: When using the consolidate drop method, consolidate peaks within 10^-*consolidate*
            of each other. See *dropmethod* for more details.

        :param float criticalerror:
            The critical error value used for warning the user of a potential calculation error.
            This only affects the ``print_details()`` function output. Default 3*10**-6 (3 parts per million)

        :param int decpl: The number of decimal places to track while calculating the isotope pattern.
            Decreasing this will improve efficiency but decrease accuracy. Options: integer.

        :param 'threshold', 'npeaks', 'consolidate' dropmethod: The peak drop method to use if desired.
            Using a peak dropping method will improve calculation times, but decrease the accuracy of the
            calculated isotope pattern. 'threshold' drops all peaks below a specified threshold value (specified using
            the *threshold* keyword argument). 'npeaks' keeps the top *n* peaks, specified by the *npeaks* keyword
            argument. 'consolidate' combines the intensity of peaks below the threshold value into the
            nearest peak (within the delta specified by the *consolidate* keyword argument, this method is the most
            accurate). The new peak *m/z* value is determined by the weighted average of the combined peaks. This will
            be repeated until the peak is above the threshold or there are no near peaks.

        :param bool emptyspec: Whether to use an empty spectrum obect. Disable this for very large molecules to
            improve calculation time.

        :param 'weighted', 'centroid' groupmethod: The grouping method to use when calculating the bar isotope pattern
            from the raw isotope pattern. Weighted calculates the peak locations using the weighted average of the *m/z*
            and intensity values. Centroid finds the center *m/z* value of a group of peaks.

        :param 'multiplicative', 'combinatorial', 'hybrid', 'cuda', ipmethod: The method to use for determining the isotope
            pattern. 'multiplicative' multiplies the existing list of intensities by each element. 'combinatorial' uses
            combinatorics and iterators to calculate each possible combination. 'hybrid' uses combinatorics to calcuate
            the pattern from each element, then multiplies those together

        :param bool keepall: Whether to keep all peaks calculated in the isotope pattern. When false, this will drop
            all intensities below 0.0001 after calculating the isotope pattern.

        :param int npeaks: The number of peaks to keep if *dropmethod* is 'npeaks'. See *dropmethod* for more details.

        :param float threshold: The threshold value determining whether or not to drop a peak. Only has an effect if
            *dropmethod* is not ``None``. See *dropmethod* for more details.

        :param bool verbose: Verbose output. Mostly useful when calculating for large molecules or while debugging.
        :param str mass_key: The mass dictionary to use for calculations. Default is nist_mass, but additional mass
            dictionaries may be defined in the mass_dictionary file and retrieved using the dictionary name
            used to define them.
        """
        # todo implement apply_threshold method for trimming resulting spectrum
        self.ipmethod = ipmethod
        self._spectrum_raw = None  # spectrum object holder
        self._raw = None  # raw isotope pattern
        self.bar_isotope_pattern = [[], []]
        self.criticalerror = criticalerror
        self.decpl = decpl
        self.dropmethod = dropmethod
        self.emptyspec = emptyspec
        self.consolidate = consolidate
        self.groupmethod = groupmethod
        self.keepall = keepall
        self.npeaks = npeaks
        self.resolution = resolution
        self.threshold = threshold
        self.save = save  # todo reimplement and detail in docstring

        if precalculated is not None:  # if precalculated values were provided, pull and set to prevent recalculation
            self._comp = precalculated['composition']
            self._spectrum_raw = precalculated['spectrum']
            self.bar_isotope_pattern = precalculated['barip']
            self._raw = precalculated['rawip']
            self._gausip = precalculated['gausip']

        Molecule.__init__(
            self,
            string,
            charge=charge,
            mass_key=mass_key,
            verbose=verbose,
        )

        if save is True:
            self.save_to_jcamp()

    def __reduce__(self):
        return (
            self.__class__,
            self.__getinitargs__(),
        )

    def __getinitargs__(self):
        return (
            self.composition,
            self.charge,
            self.consolidate,
            self.criticalerror,
            self.decpl,
            self.dropmethod,
            self.emptyspec,
            self.groupmethod,
            self.ipmethod,
            self.keepall,
            self.npeaks,
            self.resolution,
            self.threshold,
            self.save,
            self.verbose,
            {  # precalculated values
                'composition': self.composition,
                'spectrum': self.spectrum_raw,
                'rawip': self.raw_isotope_pattern,
                'barip': self.bar_isotope_pattern,
                'gausip': self.gaussian_isotope_pattern if self._gausip is not None else None,
            },
        )

    def _get_kwargs(self) -> dict:
        """gets the kwargs associated with the instance for reinstantiation"""
        return {
            'charge': self.charge,
            'mass_key': self.mass_key,
            'verbose': self.verbose,
            'consolidate': self.consolidate,
            'criticalerror': self.criticalerror,
            'decpl': self.decpl,
            'dropmethod': self.dropmethod,
            'emptyspec': self.emptyspec,
            'groupmethod': self.groupmethod,
            'ipmethod': self.ipmethod,
            'keepall': self.keepall,
            'npeaks': self.npeaks,
            'resolution': self.resolution,
            'threshold': self.threshold,
            'save': self.save,
        }

    @property
    def ipmethod(self):
        return self._ipmethod

    @ipmethod.setter
    def ipmethod(self, value):
        if value not in VALID_IPMETHODS:
            raise ValueError(f'The isotope pattern generation method {value} is not valid. ipmethod must be one '
                             f'of: {", ".join(VALID_IPMETHODS)}')
        self._ipmethod = value

    @property
    def dropmethod(self):
        return self._dropmethod

    @dropmethod.setter
    def dropmethod(self, value):
        if value not in VALID_DROPMETHODS:
            raise ValueError(f'The intensity dropping method {value} is not valid. dropmethod must be one '
                             f'of: {", ".join(VALID_DROPMETHODS)}')
        self._dropmethod = value

    @property
    def estimated_exact_mass(self):
        """determines the precise exact mass from the bar isotope pattern"""
        ind = self.bar_isotope_pattern[1].index(
            max(self.bar_isotope_pattern[1])
        )
        return self.bar_isotope_pattern[0][ind]

    @property
    def em(self):
        """Legacy attribute access: estimated exact mass"""
        return self.estimated_exact_mass

    @property
    def molecular_weight_estimated(self):
        """The molecular weight of the molecule estimated by the isotope pattern"""
        return pattern_molecular_weight(
            *self.raw_isotope_pattern,
            charge=self.charge,
        )

    @property
    def pmw(self):
        """Legacy retrieval of pattern molecular weight"""
        return self.molecular_weight_estimated

    @property
    def error(self):
        """Error of the generated isotope pattern"""
        return molecular_weight_error(
            calculated=self.molecular_weight_estimated,
            expected=self.molecular_weight,
        )

    @property
    def sigma(self):
        """Standard deviation of the isotope pattern"""
        return standard_deviation(self.fwhm)

    @property
    def nominal_mass(self):
        """the nominal mass of the molecule"""
        return int(round(self.em))

    @property
    def fwhm(self):
        try:  # try to return from estimated, unless uncalculated, use monoisotopic
            return self.estimated_exact_mass / self.resolution
        except (IndexError, ValueError):
            return self.monoisotopic_mass / self.resolution

    @property
    def barip(self):
        """Legacy attribute access"""
        return self.bar_isotope_pattern

    @property
    def raw_isotope_pattern(self):
        if self._raw is None:
            self._raw = self.spectrum_raw.trim()
        return self._raw

    @property
    def rawip(self):
        """Legacy attribute access"""
        return self.raw_isotope_pattern

    @property
    def spectrum_raw(self):
        return self._spectrum_raw

    @property
    def gaussian_isotope_pattern(self):
        if self._gausip is None:  # if it hasn't been calculated, generate
            self._gausip = gaussian_isotope_pattern(
                self.bar_isotope_pattern,
                self.fwhm
            )
        return self._gausip

    @property
    def gausip(self):
        """Legacy retrieval"""
        return self.gaussian_isotope_pattern

    @property
    def composition(self):
        return self._comp

    @composition.setter
    def composition(self, dct):
        if type(dct) != dict:
            raise TypeError('The composition must be a dictionary')
        if dct == self.composition:  # do nothing if the composition dictionary is the same as current
            return
        dct = copy.copy(dct)
        dct = abbreviations(dct)  # check for and convert abbreviations
        if 'charge' in dct:  # if charge was specified in the formula
            self.charge, self.sign = interpret_charge(dct['charge'])
            del dct['charge']
        check_in_mass_dict(dct)  # check in mass dictionary
        self._comp = dct  # set local dictionary
        self._calculate_ips()  # calculate isotope patterns
        # todo save to pickle

    @property
    def isotope_pattern_standard_deviation(self):
        """
        Cacluates the standard deviation of the isotope pattern of the supplied composition
        this calculation is based on Rockwood and Van Orden 1996 doi: 10.1021/ac951158i
        """
        return np.sqrt(
            sum([
                intensity * (mz - self.pmw) ** 2  # weighted distance from the estimated molecular weight
                for mz, intensity in zip(*self.raw_isotope_pattern)
            ])
        )

    @property
    def bounds(self):
        """Convenient attribute access to default bounds. Call calculate_bounds for additional options. """
        return self.calculate_bounds()

    @property
    def per_peak_bounds(self):
        """Convenient attribute access to per-peak bounds. Call calculate_bounds for additional options. """
        return self.calculate_bounds(perpeak=True)

    def calculate_bounds(
            self,
            conf: float = 0.95,
            perpeak: bool = False,
            threshold: float = 0.01
    ):
        """
        Calculates the *m/z* bounds of the isotope pattern of the molecule object based
        on a confidence interval and the *m/z* values of the bar isotope pattern.
        This can be used to automatically determine the integration bounds required to
        contain XX% of the counts associated with that molecule in a mass spectrum.

        :param conf: The confidence interval to use for calculating the bounds.
            e.g. *0.95* corresponds to a 95% confidence interval.
        :param perpeak: Whether or not to return the bounds required to integrate each
            peak of the isotope pattern individually.
            This can be useful in a very noisy mass spectrum to avoid
            baseline noise within the integration interval.
        :param threshold: The threshold used to determine whether a peak should be
            included in the bounds.
        :return: bounds.
            If *perpeak* is False, this will return a two item list
            corresponding to the start and end *m/z* bounds.
            If *perpeak* is True, returns a dictionary of bounds with
            the key format of
            ``dict[parent m/z value]['bounds'] = [start m/z, end m/z]``

        **Examples**

        To determine the integration bounds of C61H51IP3Pd:

        ::

            >>> mol = IPMolecule('C61H51IP3Pd')
            >>> mol.calculate_bounds(0.95)
            [1104.9458115053008, 1116.3249999321531]

            >>> mol.calculate_bounds(0.99)
            [1104.8877964620444, 1116.3830149754094]

            >>> mol.calculate_bounds(0.95, True)
            {'1105.1304418': {'bounds': (1104.9458115053008, 1105.3150720946992)},
            '1106.13382235': {'bounds': (1105.9491920547823, 1106.3184526441808)},
            '1107.12903188': {'bounds': (1106.9444015896975, 1107.3136621790959)},
            '1108.13051519': {'bounds': (1107.9458848935217, 1108.3151454829201)},
            '1109.13037767': {'bounds': (1108.9457473736579, 1109.3150079630564)},
            '1110.13288962': {'bounds': (1109.9482593265234, 1110.3175199159218)},
            '1111.13024042': {'bounds': (1110.9456101206658, 1111.3148707100643)},
            '1112.13263766': {'bounds': (1111.9480073654438, 1112.3172679548422)},
            '1113.13193341': {'bounds': (1112.9473031156144, 1113.3165637050129)},
            '1114.13415503': {'bounds': (1113.9495247326277, 1114.3187853220261)},
            '1115.13715205': {'bounds': (1114.9525217596001, 1115.3217823489986)},
            '1116.14036964': {'bounds': (1115.9557393427547, 1116.3249999321531)}}

        """
        logger.info('calculating bounds from simulated gaussian isotope pattern')
        threshold = threshold * max(self.bar_isotope_pattern[1])
        tempip = [[], []]
        for ind, inten in enumerate(self.bar_isotope_pattern[1]):  # checks for intensities above threshold
            if inten >= threshold:
                tempip[0].append(self.bar_isotope_pattern[0][ind])
                tempip[1].append(self.bar_isotope_pattern[1][ind])
        if perpeak is True:  # if per-peak bounds are called for
            out = {}
            for mz in tempip[0]:
                out[str(mz)] = {}
                out[str(mz)]['bounds'] = stats.norm.interval(conf, mz, scale=self.sigma)
        else:  # a general range that covers the entire isotope pattern
            out = [stats.norm.interval(conf, tempip[0][0], scale=self.sigma)[0],
                   stats.norm.interval(conf, tempip[0][-1], scale=self.sigma)[1]]
        logger.debug(f'caclulated bounds: {out[0]:.3f}-{out[1]:.3f}')
        return out

    def _calculate_ips(self):
        """Call to calculate isotope patterns based on the specified parameters"""
        # generates the raw isotope pattern (charge of 1)
        if self.ipmethod == 'combinatorics':
            calculator = isotope_pattern_combinatoric
        elif self.ipmethod == 'multiplicative':
            calculator = isotope_pattern_multiplicative
        elif self.ipmethod == 'hybrid':
            calculator = isotope_pattern_hybrid
        # elif self.ipmethod == 'cuda':
        #     calculator = isotope_pattern_cuda
        elif self.ipmethod == 'isospec':
            calculator = isotope_pattern_isospec
        else:
            raise ValueError(f'The isotope pattern method {self.ipmethod} is not valid')

        self._spectrum_raw = calculator(
            self.composition,
            decpl=self.decpl,
            verbose=self.verbose,
            dropmethod=self.dropmethod,
            threshold=self.threshold,
            npeaks=self.npeaks,
            consolidate=self.consolidate,
            fwhm=self.fwhm,
        )

        # apply charge
        self.spectrum_raw.charge = self.charge

        # generate bar isotope pattern based on the raw pattern
        self.bar_isotope_pattern = bar_isotope_pattern(
            self.raw_isotope_pattern,
            self.fwhm
        )
        if abs(self.error) > self.criticalerror:
            logger.warning(f'the estimated pattern error of {self} is {self.error} (critical: {self.criticalerror})')

    def compare(self, exp):
        """
        Compares a provided mass spectrum (experimental) to the simulated gaussian
        isotope pattern. Returns a standard error of the regression as an assessment
        of the goodness of fit.

        **Parameters**

        exp: *list*
            The experimentally acquired mass spectra provided as a paired list of lists
            ``[[m/z values],[intensity values]]``


        **Returns**

        Standard error of the regression: *float*
            A measure of the average distance between the experimental and predicted
            values. Lower is better, although this is a qualitative assessment.

        """

        def sumsquare(lst):
            """calculates the sum of squares"""
            ss = 0
            for val in lst:
                ss += val ** 2
            return ss
        # TODO fix this method (worthwhile?)
        #   - 2015-09-15 06 gives a bounds error
        yvals = []
        res = []
        maxy = float(max(exp[1]))
        if maxy == 0.:
            return 'could not calculate'
        for ind, val in enumerate(exp[1]):  # normalize y values
            yvals.append(float(val) / maxy * 100.)
        # avgy = sum(exp[1])/len(exp[1])
        for ind, mz in enumerate(exp[0]):
            if min(self.gausip[0]) < mz < max(self.gausip[0]):  # if within isotope pattern
                nspind = self.spectrum_raw.index(mz)  # calculate index
                if self.spectrum_raw.y[nspind] is not None:  # if the predicted intensity is not None
                    # difference between observed and predicted (residuals)
                    res.append(yvals[ind] - self.spectrum_raw.y[nspind])
                    # tot.append(self.spec.y[nspind]-avgy) # difference between predicted and mean
        # rsqrd = 1-(sumsquare(res)/sumsquare(tot)) # r-squared value (apparently not applicable to non-linear fits)
        return np.sqrt(sumsquare(res) / len(res))

    def compare_exact_mass(self, mass, use='est'):
        """
        Compares the provided mass to the exact mass of the calculated molecule.

        **Parameters**

        mass: *float*
            experimental mass to compare

        use: est or mi (optional)
            Whether to compare the estimated exact mass or the monoisotopic
            mass to the provided value. Default: est

        **Returns**

        relative error: *float*
            The relative error of the provided mass to the exact mass
        """
        if use == 'est':
            delta = mass - self.em
            return delta / self.em * 10 ** 6
        elif use == 'mi':
            delta = mass - self.mimass
            return delta / self.mimass * 10 ** 6

    def load_from_pickle(self, customfile=None):
        """loads data from pickle"""
        raise NotImplementedError('This functionality has been temporarily disabled due to significant changes in the '
                                  'class. ')
        # TODO specify hierachy and pull if better method than specified
        if customfile is None:  # if no directory was specified, use current working directory
            customfile = os.path.join(
                os.getcwd(),
                'molecules',
                self.molecular_formula(self.comp) + '.mol',
            )
        if os.path.isfile(customfile) is True:
            if self.ipmethod.lower() == 'multiplicative':
                key = 'multiplicative'
            elif self.ipmethod.lower() == 'combinatorics':
                key = 'combinatorics'
            if self.dropmethod is not None:
                key += ' %s' % self.dropmethod
            subkey = self.decpl  # decimal places
            with open(customfile, 'rb') as targetfile:
                incoming = pickle.load(targetfile)
                if key in incoming and subkey in incoming[key]:
                    items = incoming[key][subkey]
                    strcharge = '%s%d' % (self.sign, self.charge)
                    if items['charge'] == strcharge:  # if the charge combination matches
                        print('Loading data from saved file %s' % customfile)
                        pythoms.molecule.algorithms.bar.bar_isotope_pattern = items['bar isotope pattern']
                        self.raw_isotope_pattern = items['raw isotope pattern']
                        self.gausip = items['gaussian isotope pattern']
                        self.mw = items['mw']
                        self.mimass = items['monoisotopic mass']
                        self.em = items['estimated exact mass']
                        self.pcomp = items['percent composition']
                        self.error = items['error']
                        self.fwhm = items['full width at half max']
                        self.sigma = items['standard deviation']
                        self.sf = self.molecular_formula(self.comp)
                        return True
        return False  # if the exact match was not found, False

    def print_details(self):
        """prints the details of the generated molecule"""
        print(f'{self}')
        print(f'formula: {self.molecular_formula}')
        print(f'molecular weight: {round(self.molecular_weight, self.decpl)}')
        print(f'monoisotopic mass: {round(self.monoisotopic_mass, self.decpl)}')
        print(f'estimated exact mass: {round(self.estimated_exact_mass, self.decpl)}')
        print(f'error: {self.error:.3}')
        if abs(self.error) > self.criticalerror:
            print(f'WARNING: Error is greater than {self.criticalerror}!')
        print('')
        self.print_percent_composition()

    def plot_bar_pattern(self):
        """plots and shows the isotope bar pattern"""
        fwhm = self.em / self.resolution
        pl.bar(self.bar_isotope_pattern[0], self.bar_isotope_pattern[1], width=fwhm, align='center')
        pl.xlabel('m/z', style='italic')
        pl.ylabel('normalized intensity')
        pl.ticklabel_format(useOffset=False)
        pl.show()

    def plot_gaussian_pattern(self, exp=None):
        """plots and shows the simulated gaussian isotope pattern"""
        pl.plot(*self.gaussian_isotope_pattern, linewidth=1)
        if exp is not None:  # plots experimental if supplied
            y = []
            maxy = max(exp[1])
            for val in exp[1]:  # normalize
                y.append(val / maxy * 100)
            comp = self.compare(exp)
            pl.plot(exp[0], exp[1])
            pl.text(max(exp[0]), 95, 'SER: ' + str(comp))
            # pl.fill_between(x,self.gausip[1],exp[1],where= exp[1] =< self.gausip[1],interpolate=True, facecolor='red')
        pl.fill(self.gausip[0], self.gausip[1], alpha=0.25)  # ,facecolor='blue')
        pl.xlabel('m/z', style='italic')
        pl.ylabel('normalized intensity')
        pl.ticklabel_format(useOffset=False)
        pl.show()

    def plot_raw_pattern(self):
        """plots and shows the raw isotope pattern (with mass defects preserved)"""
        pl.bar(self.raw_isotope_pattern[0], self.raw_isotope_pattern[1], width=self.fwhm)
        pl.xlabel('m/z', style='italic')
        pl.ylabel('normalized intensity')
        pl.ticklabel_format(useOffset=False)
        pl.show()

    def save_to_jcamp(self, name=None):
        """
        Saves the bar isotope pattern to JCAMP-DX file format
        Output type roughly based on the output from ChemCalc.org
        see http://www.jcamp-dx.org/protocols.html for details on the JCAMP-DX specifications.

        :param name: optional name for the output file (default is {molecular formula}.jdx)
        """
        if os.path.isdir(os.path.join(os.getcwd(), 'molecules')) is False:
            os.makedirs(os.path.join(os.getcwd(), 'molecules'))
        if name is None:  # if no name supplied, auto generate
            name = self.molecular_formula
            name += '.jdx'
        elif name.lower().endswith('.jdx') is False:
            name += '.jdx'

        logger.info(f'saving {name} to {os.path.join(os.getcwd(), "molecules")}')

        header = [  # comment lines to put before data
            # header items
            f'TITLE= {self.molecular_formula}',
            'JCAMP-DX= 5.01',
            'DATA TYPE= MASS SPECTRUM',
            'DATA CLASS= PEAK TABLE',
            f'ORIGIN= Calculated spectrum from PythoMS {self.__class__} class https://github.com/larsyunker/PythoMS',
            f'OWNER= {os.getlogin()}',
            f'SPECTROMETER/DATA SYSTEM= {self.__class__} class {self.ipmethod} method',
            f'CREATION DATE= {datetime.now().astimezone()}',
            'XUNITS= M/Z',
            'YUNITS= RELATIVE ABUNDANCE',
            f'NPOINTS= {len(self.bar_isotope_pattern[0])}',
            f'FIRSTX= {self.bar_isotope_pattern[0][0]}',
            f'LASTX= {self.bar_isotope_pattern[0][1]}',

            # user defined labels
            f'$Molecular weight= {self.molecular_weight}',
            f'$Resolution= {self.res}',
            f'$Threshold= {self.threshold if self.threshold is not None else ""}',
            f'$Error= {self.error:.2}',
            f'$Nominal mass = {self.nominal_mass}',
            f'$Monoisotopic mass= {self.monoisotopic_mass}',
            f'$Estimated exact mass= {self.estimated_exact_mass}',
        ]
        with open(os.path.join(os.getcwd(), "molecules", name), 'wt') as outfile:
            for line in header:  # write header lines
                if len(line) != 0:
                    outfile.write(f'##{line}\n')
            outfile.write('##PEAK TABLE= (XY..XY)\n')
            for mz, intensity in zip(*self.bar_isotope_pattern):  # write data lines
                outfile.write(f'{mz}, {intensity}\n')
            outfile.write('##END=\n')

    def save_to_pickle(self, name=None):
        """
        Saves the molecule's properties to pickle
        """
        if os.path.isdir(os.path.join(os.getcwd(), 'molecules')) is False:
            os.makedirs(os.path.join(os.getcwd(), 'molecules'))
        if name is None:  # if no name supplied, auto generate
            name = self.molecular_formula
            name += '.mol'
        elif name.lower().endswith('.mol') is False:
            name += '.mol'

        logger.info(f'saving {name} to {os.path.join(os.getcwd(), "molecules")}')

        with open(os.path.join(os.getcwd(), "molecules", name), 'wb') as outfile:
            pickle.dump(
                self,
                outfile
            )

        # todo differentiate between generation methods in the output files
