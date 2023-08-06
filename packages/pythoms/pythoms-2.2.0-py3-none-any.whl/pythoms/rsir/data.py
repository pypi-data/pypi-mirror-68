"""module for managing data and attributes required for RSIR analysis"""
import re
from typing import Union, List, Tuple, Iterable

import numpy as np
from openpyxl.cell import Cell
import matplotlib.pyplot as plt

from ..molecule import IPMolecule
from ..mzml.structure import mzML, Trace
from ..spectrum import Spectrum
from ..tome import slice_array, normalize


# pattern kwarg map
_kwarg_map = {
    'name': 'name',
    'function': 'func(tion)?',
    'affinity': 'affin(ity)?',
    'formula': '(molecular([\s_])?)?formula',
}
_kwarg_map = {
    key: re.compile(pattern, re.IGNORECASE)
    for key, pattern in _kwarg_map.items()
}


# regex for start and end mz
_start_mz_re = re.compile(
    '(mz)?start([-_])?(mz)?',
    re.IGNORECASE
)
_end_mz_re = re.compile(
    '(mz)?end([-_])?(mz)?',
    re.IGNORECASE
)


def _find_column(header_row: Iterable[Cell], pattern: re.Pattern):
    """
    Finds the column index which matches the pattern

    :param header_row: row of cells in the header of an Excel file
    :param pattern: regex pattern
    :return: column index for value
    """
    for ind, cell in enumerate(header_row):
        val = cell.value
        if val is None:
            continue
        if pattern.search(val):
            return ind
    return None


def _find_columns(header_row: Iterable[Cell]) -> dict:
    """
    Finds the column indicies for RSIRTarget kwargs

    :param header_row: row of cells in the header of an Excel file
    :return: kwarg/column index map
    """
    out = {}
    # find standard mappings
    for key, pattern in _kwarg_map.items():
        ind = _find_column(header_row, pattern)
        if ind is not None:
            out[key] = ind
    return out


def get_bounds(row: Iterable[Cell], header_row: Iterable[Cell]):
    """
    Gets the bounds from a species row based on the header row

    :param header_row: row of cells in the header of an Excel file
    :param row: row to search
    :return: bounds
    """
    out = [None, None]
    for ind, header_cell in enumerate(header_row):
        value = header_cell.value
        if value is None:
            continue
        if _start_mz_re.search(header_cell.value) is not None:
            out[0] = row[ind].value
        if _end_mz_re.search(header_cell.value) is not None:
            out[1] = row[ind].value
    # if values were found, return out, otherwise return None
    if any(val is not None for val in out):
        return out
    return None


def get_kwargs_from_row(row: Iterable[Cell],
                        column_map: dict,
                        header_row: Iterable[Cell],
                        ) -> dict:
    """
    Retrieves RSIRTarget kwargs from a row

    :param row: excel row
    :param column_map: column map for the sheet
    :param header_row: row of cells in the header of an Excel file
    :return: instantiation kwargs for RSIRTarget
    """
    out = {}
    for key, ind in column_map.items():
        val = row[ind].value
        if val is not None:
            out[key] = val
    out['bounds'] = get_bounds(row, header_row)
    return out


def expand_bounds(left: float, right: float, value: float) -> List[float]:
    """
    Expands the provided bounds by the provided value

    :param left: left bound
    :param right: right bound
    :param value: expansion value
    :return: new bounds
    """
    return [
        left - value,
        right + value,
    ]


def visualize_target_bounds(spectrum: Union[Spectrum, List],
                            target: 'RSIRTarget',
                            ip_style='bar',
                            ) -> Tuple[plt.Figure, plt.Axes]:
    """
    Visualizes the target bounds overlaid on the spectrum.

    :param spectrum: Spectrum instance or [x,y] list of the spectrum
    :param target: RSIR target instance
    :param ip_style: isotope pattern style to plot (bar or gaussian)
    :return: figure, axes
    """
    fig, ax = plt.subplots()
    if isinstance(spectrum, Spectrum):
        spectrum = spectrum.trim()
    ax.plot(
        *spectrum
    )
    for bound in target.bounds:
        ax.axvline(bound, color='r', linestyle='-')
        # todo include bound label
    if target.molecule is not None:
        if ip_style.lower() == 'gaussian':
            gausip = target.molecule.gaussian_isotope_pattern
            gausip[1] = normalize(
                gausip[1],
                max(spectrum[1])
            )
            ax.fill(
                *gausip,
                alpha=0.25
            )
        elif ip_style.lower() == 'bar':
            barip = target.molecule.bar_isotope_pattern
            barip[1] = normalize(
                barip[1],
                max(spectrum[1])
            )
            ax.bar(
                *barip,
                width=target.molecule.fwhm,
                align='center',
                alpha=0.25,
            )
    # expand bounds by 1
    ax.set_xlim(*expand_bounds(*target.bounds, 1))
    ax.set_ylabel('intensity')
    ax.set_xlabel('m/z')
    ax.set_title(target.name)
    fig.tight_layout()
    # todo set ylim
    return fig, ax


class RSIRTarget:
    # precision to use for sumspectrum
    SPECTRUM_PRECISION = 3

    def __init__(self,
                 formula: Union[IPMolecule, str] = None,
                 bounds: List[float] = None,
                 affinity: str = None,
                 function: int = None,
                 store_spectra: bool = False,
                 name: str = None,
                 level: int = 1,
                 conf_interval: float = 0.95,
                 resolution: float = 5000,
                 expand_bounds: float = 0.,
                 ):
        """
        Data class for RSIR data

        :param formula: molecular formula (or IPMolecule instance)
        :param bounds: manually specified bounds
        :param affinity: MS mode affinity (+ or -)
        :param function: MS function to find the data in
        :param store_spectra: flag to enable spectral storage if desired. If enabled, creates a Spectrum object
            associated with the instance.
        :param name: species name
        :param level: MSn level (unless you're performing MS/MS experiments, this will be 1)
        :param conf_interval: confidence interval for use in automatic bounds determination
        :param resolution: resolution to use for bounds determination using IPMolecule instances
        :param expand_bounds: parameter for automatically expanding bounds by some value. For example, if the bounds are
            automatically determined from a molecule instance, the determined bounds will be expanded by 2* this value.
        """
        # todo support manually specified resolution
        self._molecule: IPMolecule = None
        self._bounds = None
        self._affinity = None
        self._name = None
        # bounds error counter
        self._bounds_warnings = 0
        self._store_spectra = False
        self._spectrum: Spectrum = None
        self._conf_interval = conf_interval

        self.expand_bounds = expand_bounds
        self.name = name
        self.formula = formula
        self.resolution = resolution
        self.bounds = bounds
        self.affinity = affinity
        self.function = function
        self.level = level
        self.conf_interval = conf_interval

        # storage container for raw data
        self.raw_data = Trace()

        self.store_spectra = store_spectra

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    @property
    def name(self) -> str:
        """species name"""
        if self._name is not None:
            return self._name
        elif self._molecule is not None:
            return self._molecule.molecular_formula
        elif self._bounds is not None:
            out = f'm/z {self._bounds[0]:.1f}'
            if self._bounds[1] is not None:
                out += f' - {self._bounds[1]:.1f}'
            return out
        return 'unnamed'

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = str(value)

    @name.deleter
    def name(self):
        self.name = None

    @property
    def formula(self) -> IPMolecule:
        """molecule object to reference"""
        return self._molecule

    @formula.setter
    def formula(self, value: Union[IPMolecule, str]):
        if value is None:
            self._molecule = None
        else:
            self._molecule = IPMolecule(value)

    @formula.deleter
    def formula(self):
        self._molecule = None

    @property
    def bounds(self) -> List[float]:
        """m/z bounds to use for intensity tracking"""
        # return manually set bounds if specified
        if self._bounds is not None:
            out = self._bounds
        # or determined bounds from molecule class
        elif self._molecule is not None:
            out = self._molecule.calculate_bounds(
                conf=self.conf_interval,
            )
        else:
            raise AttributeError(f'Bounds have not been set for this instance')
        return expand_bounds(
            *out,
            self.expand_bounds,
        )

    @bounds.setter
    def bounds(self, value: List[float]):
        if value is None:
            self._bounds = None
            return
        # if a single value was specified
        if len(value) != 2:
            raise ValueError('current functionality requires bounds to be fully specified')
            # todo enable ability to just specify single m/z
            value = [value, None]
        # if two values were specified, check range
        elif value[0] > value[1]:
            raise ValueError('the start m/z must be less than the end m/z')
        self._bounds = value

    @bounds.deleter
    def bounds(self):
        self.bounds = None

    @property
    def bounds_warnings(self) -> int:
        """count of the number of bounds warnings during processing"""
        return self._bounds_warnings

    @property
    def affinity(self) -> str:
        """MS type affinity (+/-/UV)"""
        return self._affinity

    @affinity.setter
    def affinity(self, value: str):
        if value is None:
            self._affinity = None
        else:
            if value not in ['+', '-', 'UV']:
                raise ValueError(f'the provided value "{value}" is not a valid affinity (+, -, or UV)')
            self._affinity = value

    @property
    def store_spectra(self) -> bool:
        """whether to store spectra when processing"""
        return self._store_spectra

    @store_spectra.setter
    def store_spectra(self, value: bool):
        if value is True and self._spectrum is None:
            bounds = self.bounds
            self._spectrum = Spectrum(
                self.SPECTRUM_PRECISION,
                start=bounds[0],
                end=bounds[1],
            )
        self._store_spectra = value

    @property
    def spectrum(self) -> Spectrum:
        """spectrum object associated with the instance"""
        return self._spectrum

    @property
    def molecule(self) -> IPMolecule:
        """molecule instance associated with the target (only applicable if a formula is being used)"""
        return self._molecule

    @property
    def resolution(self):
        """resolution associated with the instance"""
        if self.molecule is not None:
            return self.molecule.resolution

    @resolution.setter
    def resolution(self, value):
        if self.molecule is not None:
            self.molecule.resolution = value

    @property
    def confidence_interval(self) -> float:
        """confidence interval to use when determining bounds from an IPMolecule instance"""
        return self._conf_interval

    @confidence_interval.setter
    def confidence_interval(self, value: float):
        self._conf_interval = value

    def pull_from_mzml(self, mzml: mzML):
        """
        Retrieves corresponding data from an mzML file. The instance will automatically associate itself with the
        appropriate mzML function.

        :param mzml: mzML instance
        """
        pass

    def add_from_spectrum(self, x: Union[np.ndarray, List[float]], y: Union[np.ndarray, List[float]]):
        """
        Finds location within the the array and integrates, appending that value to the list of raw data.

        :param x: x array
        :param y: y array
        :return:
        """
        # casting to array is highly inefficient with the current structure but it works
        if isinstance(x, np.ndarray) is False:
            x = np.asarray(x)
        if isinstance(y, np.ndarray) is False:
            y = np.asarray(y)
        # slice array
        self_slice = slice_array(
            y,
            x,
            *self.bounds

        )
        if self.spectrum is not None:
            self.spectrum.add_spectrum(*self_slice)
        intensity = self_slice[1].sum()
        self.raw_data.append(intensity)
        return intensity

    def get_binned_data(self, bin_num: int) -> List[float]:
        """
        Bins the raw data into the averaged bins of the provided number (smoothing by average). Note that if the last
        bin is not of the size prescribed by bin_num, the last bin will be excluded from the result.

        :param bin_num: number of consecutive scans to bin.
        :return: list of binned intensities
        """
        return self.raw_data.get_binned_data(bin_num)

    def visualize_bounds(self, spectrum: Union[Spectrum, List], ip_style: str = 'bar') -> Tuple[plt.Figure, plt.Axes]:
        """
        Visualizes the bounds of the species overlaid on the provided spectrum

        :param spectrum: Spectrum instance or [x,y] list of the spectrum
        :param ip_style: isotope pattern style to plot (bar or gaussian)
        :return: figure, axes
        """
        return visualize_target_bounds(
            spectrum,
            target=self,
            ip_style=ip_style,
        )
