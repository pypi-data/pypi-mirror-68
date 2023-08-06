from tqdm import tqdm

from ..settings import VERBOSE
from ..util import autodec, normal_distribution
from ..logging import logger
from ...spectrum import Spectrum


def gaussian_isotope_pattern(
        barip: list,
        fwhm: float,
        verbose: bool = VERBOSE,
):
    """
    Simulates the isotope pattern that would be observed in a mass
    spectrometer with the resolution specified as a fwhm value.

    :param barip: The isotope pattern to be simulated. This can be either the bar isotope
        pattern or the raw isotope pattern (although this will be substantially
        slower for large molecules).
    :param fwhm: full-width-at-half-maximum
    :param verbose: chatty mode
    :return: The predicted gaussian isotope pattern in the form of a paired list
        ``[[m/z values],[intensity values]]``
    :rtype: list
    """
    logger.info('generating gaussian isotope pattern')
    spec = Spectrum(  # generate Spectrum object to encompass the entire region
        autodec(fwhm),
        start=min(barip[0]) - fwhm * 2,
        end=max(barip[0]) + fwhm * 2,
        empty=False,  # whether or not to use emptyspec
        filler=0.,  # fill with zeros, not None
    )
    msg = 'calculating gaussian isotope pattern'
    # generate normal distributions for each peak
    for ind, val in enumerate(tqdm(barip[0], desc=msg, total=len(barip[0]), disable=not verbose)):
        nd = normal_distribution(val, fwhm, barip[1][ind])  # generate normal distribution for that peak
        spec.add_spectrum(nd[0], nd[1])  # add the generated spectrum to the total spectrum
    spec.normalize()  # normalize
    gausip = spec.trim()  # trim None values and output
    logger.info('gaussian isotope pattern generation complete')
    return gausip