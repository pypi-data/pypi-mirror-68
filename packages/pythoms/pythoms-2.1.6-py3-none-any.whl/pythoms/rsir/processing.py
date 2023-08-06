"""
module for performing multi-RSIR analysis on an mzML instance
"""

import logging
import pathlib
import warnings
from functools import wraps
import matplotlib.pyplot as plt
from typing import Union, List, Tuple, Callable, Iterable, Mapping

import numpy as np
from openpyxl.cell import Cell
from tqdm import tqdm

from ..mzml import mzML
from ..mzml.parsing import spectrum_array, fps
from ..tome import bindata, normalize_lists
from ..xlsx import XLSX
from ..spectrum import Spectrum
from .data import RSIRTarget, _find_columns, get_kwargs_from_row

# module logger
logger = logging.getLogger(__name__)


def _write_data_and_normalize_data(xlfile: XLSX,
                                   time_list: Iterable[float],
                                   tic_list: Iterable[float],
                                   *species_data: Iterable[float],
                                   species_names: List[str] = None,
                                   sheet_base_name: str = None,
                                   ):
    """
    Writes both the provided data and the data normalized to the TIC to separate sheets

    :param xlfile: XLSX instance or file path to excel file
    :param species_names: names to use for headers
    :param time_list: list of time points
    :param tic_list: list of total ion current points
    :param species_data: list of data points for each species
    """
    if species_names is None:
        species_names = [f'species {i + 1}' for i, lst in enumerate(species_data)]
    if sheet_base_name is None:
        sheet_base_name = 'data'

    # todo append time units in header
    # write raw data
    arr = np.asarray([
        time_list,
        tic_list,
        *species_data
    ])
    xlfile.write_array_to_sheet(
        arr=arr.T,
        header_row=['Time', 'TIC', *species_names],
        sheetname=f'{sheet_base_name} raw data',
        save=False,
    )

    # normalize and write data
    norm_arr = np.asarray([
        time_list,
        *[normalize_lists(species, tic_list) for species in species_data]
    ])
    xlfile.write_array_to_sheet(
        norm_arr.T,
        header_row=['Time', *species_names],
        sheetname=f'{sheet_base_name} normalized',
        save=False,
    )


def targets_from_xlsx(xlfile: Union[str, pathlib.Path, XLSX],
                      sheet: str = 'parameters',
                      ) -> List[RSIRTarget]:
    """
    Loads reconstructed single ion monitoring parameters from the specified sheet.

    :param xlfile: excel file or path to excel file
    :param sheet: sheet name to read from
    :return: RSIRTarget instances

    **Valid column headings**

    There are several valid column headings that are recognized by this function.

    Name: name of the species
        This will be the dictionary key in the returned parameters dictionary.

    Formula: chemical formula
        The molecular formula for a given species can be provided, and the
        integration bounds will be automatically generated using the simulated
        isotope pattern. See ``Molecule.bounds()`` method for more details.

    Function: function in the mzML
        This can be specified if the function in the mass spec acquisition file
        is known. The function number can usually be viewed using the instrument
        manufacturers software or a program like ProteoWizard's seeMS.
        This is optional unless there is more than one spectrum type which matches
        the provided affinity.

    Affinity: the spectrum type where the species can be found
        This must be specified to indicate which mass spectrum type to look for
        the assigned species.
        Options: '+' (positive mode),'-' (negative mode), or 'UV' (UV-Vis channel).
        e.g. if the species is positively charged, specify '+'.
        If no affinity is specified, positive mode is assumed.

    Start: the integration start point
        The integration start point must be manually assigned if a molecular
        formula was not specified. The PyRSIR scipt will integrate values
        between the x values specified by *start* and *end*.
        If you wish to integrate only a single x value, specify the start
        value and leave the end value blank.

    End: the integration stop point
        The integration start point must be manually specified if a molecular
        formula was not provided.

    **Requirements for PyRSIR**

    At least one of *name*, *formula*, *start*, or *end* must be specified for
    PyRSIR to function.

    The excel sheet is expected to have the first row defining the columns
    (see above) and any subsequent row defining one species to track per
    line.
    """
    if isinstance(xlfile, XLSX) is False:
        xlfile = XLSX(xlfile)

    s = xlfile.wb[sheet]  # load sheet in specified excel file
    rows: List[Cell] = list(s.rows)
    header_map = _find_columns(rows[0])

    targets: List[RSIRTarget] = []
    for row in rows[1:]:
        targets.append(RSIRTarget(
            **get_kwargs_from_row(
                row,
                header_map,
                rows[0]
            )
        ))
    return targets


class RSIR:
    # precision number for full spectrum storage
    FULL_SPECTRUM_PRECISION: int = 3

    def __init__(self,
                 mzml_file: Union[str, pathlib.Path, mzML],
                 bin_numbers: List[int] = None,
                 store_isotope_patterns: bool = True,
                 store_full_spectra: bool = False,
                 bounds_confidence: float = 0.99,
                 **kwargs,
                 ):
        """
        Class for performing one or more Reconstructed Single Ion Recording (RSIR) analyses on an mzML file.
        Targets are defined by the RSIRTarget class.

        :param mzml_file: target mzML file to process
        :param bin_numbers: list of bin numbers for adjacent-scan binning
        :param store_isotope_patterns: toggle for storing cumulative isotope patterns for each target
        :param store_full_spectra: toggle for storing the full spectrum of each function
        :param bounds_confidence: bounds confidence level to use when automatically determining bounds from IPMolecule
            instances
        :param kwargs: kwarg legacy catch
        """
        # todo support loading of raw data
        # flag for denoting whether RSIR has been run
        self._processed: bool = False
        self._mzml: mzML = None
        self._targets = []
        self._bin_numbers: List[int] = []
        self._store_full_spec = False
        self.full_spectra: Mapping[int, Spectrum] = {}
        self.logger = logger.getChild(self.__class__.__name__)  # todo logger child from mzml filename
        self.mzml = mzml_file
        self.mzml.extract_function_time_tic()
        if 'n' in kwargs:
            warnings.warn(  # v2.1.0
                'the "n" kwarg will be deprecated, please use "bin_numbers" instead',
                DeprecationWarning,
                stacklevel=2,
            )
            if bin_numbers is None:
                bin_numbers = kwargs['n']
        self.bin_numbers = bin_numbers
        # confidence interval for automatically generated bounds (from IPMolecule)
        self.bounds_confidence: float = bounds_confidence
        self.store_isotope_patterns: bool = store_isotope_patterns
        self.store_full_spectra = store_full_spectra

    @property
    def mzml(self) -> mzML:
        """loaded mzML file"""
        return self._mzml

    @mzml.setter
    def mzml(self, value: Union[str, pathlib.Path, mzML]):
        if value is None:
            self.logger.debug(f'setting mzml to None from {self._mzml}')
            self._mzml = None
            return
        elif isinstance(value, mzML) is False:
            self.logger.debug(f'creating mzML instance from {value}')
            value = mzML(value)
        self.logger.debug(f'setting mzML property to {value}')
        self._mzml = value

    @property
    def bin_numbers(self) -> List[int]:
        """list of number of scans to bin for each target"""
        return self._bin_numbers

    @bin_numbers.setter
    def bin_numbers(self, value: Union[int, List[int]]):
        if value is None:
            self._bin_numbers = []
            return
        if type(value) is not list:
            value = list(value)
        # cast to integer
        self.logger.debug(f'bin numbers changed to {value}')
        self._bin_numbers = [int(val) for val in value]

    @property
    def targets(self) -> List[RSIRTarget]:
        """list of RSIR targets"""
        return self._targets

    @property
    def store_full_spectra(self) -> bool:
        """flag for full spectrum accumulation"""
        return self._store_full_spec

    @store_full_spectra.setter
    def store_full_spectra(self, value: bool):
        # todo consider creating a designated class to associate a spectrum to a mzML function
        # todo accept kwargs to use for instantiating Spectrum instances (e.g. narrow bounds, specify precision, etc.)
        if value is True and len(self.full_spectra) == 0:
            for func in self.mzml.functions:
                self.full_spectra[func] = Spectrum(
                    self.FULL_SPECTRUM_PRECISION,
                    *self.mzml.functions[func]['window'],
                )
        self._store_full_spec = value

    def add_target(self, target: Union[RSIRTarget, dict]):
        """
        Adds a target to the list of RSIRTargets in the instance

        :param target: RSIR target or kwargs for instantiation
        """
        if type(target) is dict:
            target = RSIRTarget(**target)
        self.logger.debug(f'adding {target} as RSIR target')
        self._targets.append(
            target
        )

    def add_targets_from_xlsx(self, xlfile, sheet='parameters'):
        """
        Adds targets as specified in an xlsx file

        :param xlfile: excel file or path to excel file
        :param sheet: sheet name to read from
        """
        self.logger.debug(f'retrieving targets from {xlfile}')
        targets = targets_from_xlsx(
            xlfile=xlfile,
            sheet=sheet,
        )
        for target in targets:
            target.store_spectra = self.store_isotope_patterns
            target.conf_interval = self.bounds_confidence
            self.add_target(target)

    def _check_processed(fn: Callable):
        """checks if the data has been processed and prevents execution otherwise"""
        @wraps(fn)
        def decorated(self: 'RSIR', *args, **kwargs):
            if self._processed is False:
                self.logger.error('data has not yet been processed, raising ValueError')
                raise ValueError(
                    f'the data has not been processed. Please run extract_data prior to calling {fn.__name__}'
                )
            return fn(self, *args, **kwargs)
        return decorated

    def extract_data(self,
                     resolution_override: float = None,
                     ):
        """
        Extracts data from the loaded mzML file.

        :param resolution_override: optional specification of the resolution to use for calculating integration bounds
            from IPMolecule instances. If not specified, the resolution will be automatically calculated from
            the mzML file.
        """
        if self.mzml is None:
            self.logger.error('an mzML instance has not been loaded')
            raise AttributeError('an mzML is not loaded for this instance')

        self.logger.info('initiating data extraction')
        # perform presteps
        autores = resolution_override
        self.logger.debug(f'using resolution of {autores}')

        self.logger.info('automatically associating targets with functions')
        for target in self.targets:
            # associate targets to functions
            if target.function is None:
                target.function = self.mzml.associate_to_function(
                    affin=target.affinity,
                    level=target.level,
                )
            if target.affinity is None:
                target.affinity = self.mzml.functions[target.function]["mode"]
            # set resolution to that of the mzml instance
            if target.molecule is not None:
                if autores is None:
                    autores = self.mzml.auto_resolution()
                target.molecule.resolution = autores

        # retrieve data
        self.logger.info('extracting data from scans')
        for element in tqdm(self.mzml.spectra_elements, desc='performing rsir analysis', total=self.mzml.nscans):
            spectrum = spectrum_array(element)
            func, proc, scan = fps(element)
            for target in self.targets:
                if target.function == func:
                    target.add_from_spectrum(*spectrum)
            if self.store_full_spectra is True:
                self.full_spectra[func].add_spectrum(*spectrum)
        self.logger.info('data extraction complete')
        self._processed = True

    def bin_tic_of_function(self, function: int, bin_num: int) -> List[float]:
        """
        Bins the TIC values of the specified function

        :param function: function number
        :param bin_num: number of scans to bin
        :return: list of binned values
        """
        return self.mzml.get_tic_of_function(function).get_binned_data(bin_num)

    def bin_time_of_function(self, function: int, bin_num: int) -> List[float]:
        """
        Bins the TIC values of the specified function

        :param function: function number
        :param bin_num: number of scans to bin
        :return: list of binned values
        """
        return self.mzml.get_timepoints_of_function(function).get_binned_data(bin_num)

    @_check_processed
    def plot_results(self) -> Tuple[plt.Figure, Iterable[plt.Axes]]:
        """
        Plots the results of the RSIR analysis for quick viewing

        :return: generated figure object and axes
        """
        n_plots = len(self.bin_numbers) + 1
        fig, ax = plt.subplots(
            n_plots,
            sharex=True,
        )
        if n_plots == 1:
            ax = [ax]
        # plot raw data
        for target in self.targets:
            ax[0].plot(
                self.mzml.get_timepoints_of_function(target.function),
                target.raw_data,
                linewidth=0.75,
                label=target.name,
            )
        # todo plot tic
        # plot binned data
        for axes, bin_num in zip(ax[1:], self.bin_numbers):
            for target in self.targets:
                axes.plot(
                    self.bin_time_of_function(target.function, bin_num),
                    target.raw_data.get_binned_data(bin_num),
                    linewidth=0.75,
                    label=target.name,
                )

        # add labels
        ax[0].set_title('Raw Data')
        ax[-1].set_xlabel('time')
        fig.text(0.01, 0.5, 'intensity', va='center', rotation='vertical')
        # turn off x tick marks
        for axes in ax[:-1]:
            axes.tick_params(
                axis='x',
                labelbottom=False,
            )

        fig.tight_layout()
        return fig, ax

    @_check_processed
    def write_rsir_to_excel(self,
                            xlfile: Union[str, pathlib.Path, XLSX],
                            save: bool = True,
                            ):
        """
        Writes the RSIR data to the specified excel file. Raw data will be written in a per-function manner denoted
        by the sheet's name ("{mode} (fn {function number})"). Binned data will be written with a "{bin num} bin ..."
        prefix.

        :param xlfile: XLSX instance or path to excel file
        :param save: whether to save after writing
        """
        if isinstance(xlfile, XLSX) is False:
            xlfile = XLSX(xlfile, create=True)
        self.logger.info(f'writing data to {xlfile}')
        # for each function defined in the mzML
        for func_num, details in self.mzml.functions.items():
            # if there are targets associated with that function
            func_targets = sorted(
                [target for target in self.targets if target.function == func_num],
                key=lambda x: x.name,
            )
            if len(func_targets) > 0:
                self.logger.info(f'writing data for {len(func_targets)} targets associated with function {func_num}')
                func_time = self.mzml.get_timepoints_of_function(func_num)
                func_tic = self.mzml.get_tic_of_function(func_num)

                # write unbinned data
                _write_data_and_normalize_data(
                    xlfile,
                    func_time,
                    func_tic,
                    *[target.raw_data for target in func_targets],
                    species_names=[target.name for target in func_targets],
                    sheet_base_name=f'{details["mode"]} (fn {func_num})',
                )

                # bin data and write
                for bin_num in self.bin_numbers:
                    self.logger.debug(f'calculating and writing bin data for n={bin_num} of function {func_num}')
                    binned_time = self.bin_time_of_function(func_num, bin_num=bin_num)
                    binned_tic = self.bin_tic_of_function(func_num, bin_num=bin_num)
                    _write_data_and_normalize_data(
                        xlfile,
                        binned_time,
                        binned_tic,
                        *[
                            bindata(bin_num, target.raw_data, v=1)
                            for target in func_targets
                        ],
                        species_names=[target.name for target in func_targets],
                        sheet_base_name=f'{bin_num} bin {details["mode"]} (fn {func_num})',
                    )

        self.logger.info('finished writing rsir data')
        if save is True:
            self.logger.info('saving excel file (this may take some time)')
            xlfile.save()

    def write_isotope_patterns_to_excel(self,
                                        xlfile: Union[str, pathlib.Path, XLSX],
                                        save: bool = True,
                                        ):
        """
        Writes accumulated isotope patterns (if any) for targets to the provided excel file.

        :param xlfile: XLSX instance or path to excel file
        :param save: whether to save after writing
        """
        if isinstance(xlfile, XLSX) is False:
            xlfile = XLSX(xlfile, create=True)
        # identify any targets with retrieved isotope patterns and write those to file
        targets_with_spectra = sorted(
            [
                target for target in self.targets
                if target.spectrum is not None
            ],
            key=lambda x: x.name,
        )
        if len(targets_with_spectra) > 0:
            self.logger.info(f'writing isotope patterns to file')
            for target in targets_with_spectra:
                trimmed = target.spectrum.trim()
                xlfile.writemultispectrum(
                    *trimmed,
                    specname=target.name,
                    xunit='m/z',  # x unit
                    yunit='Intensity (counts)',  # y unit
                    sheetname='Isotope Patterns',  # sheet name
                    chart=True,  # output excel chart
                )
            self.logger.info(f'finished writing isotope patterns to file')
            if save is True:
                self.logger.info('saving excel file (this may take some time)')
                xlfile.save()

    def write_full_spectra_to_excel(self,
                                    xlfile: Union[str, pathlib.Path, XLSX],
                                    save: bool = True,
                                    ):
        """
        Writes accumulated full spectra (if any) to the provided excel file.

        :param xlfile: XLSX instance or path to excel file
        :param save: whether to save after writing
        """
        if isinstance(xlfile, XLSX) is False:
            xlfile = XLSX(xlfile, create=True)
        if self.store_full_spectra is True:
            self.logger.info(f'writing full spectra to file')
            for func, spectrum in self.full_spectra.items():
                details = self.mzml.functions[func]
                sheet_name = f'{details["type"]}{details["mode"]} {details["window"][0]}-{details["window"][1]}'
                xlfile.writespectrum(
                    *spectrum.trim(),
                    sheet=sheet_name
                )
            self.logger.info('writing full spectra to file complete')
            if save is True:
                self.logger.info('saving data to file (this may take some time)')
                xlfile.save()

    def write_all_data_to_excel(self, xlfile: Union[str, pathlib.Path, XLSX]):
        """
        Writes RSIR, isotope patterns, and full spectra to the provided excel file

        :param xlfile: XLSX instance or path to excel file
        """
        if isinstance(xlfile, XLSX) is False:
            xlfile = XLSX(xlfile, create=True)
        self.write_rsir_to_excel(xlfile, save=False)
        self.write_isotope_patterns_to_excel(xlfile, save=False)
        self.write_full_spectra_to_excel(xlfile, save=False)
        xlfile.save()

    def update_rsir_parameters(self, xlfile: Union[str, pathlib.Path, XLSX], sheet_name: str = 'parameters'):
        """
        Updates the rsir parameters defined in the Excel file with the instance's determined values.

        :param xlfile: target Excel file
        :param sheet_name: sheet name
        """
        raise NotImplementedError('this functionality is not currently supported')  # todo update rsim params

    # set as static method for everything to work
    _check_processed = staticmethod(_check_processed)
