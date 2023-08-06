from ...spectrum import Spectrum, weighted_average
from ..logging import logger
from ..util import group_masses, centroid
from ..settings import VERBOSE

logger = logger.getChild(__name__)


# valid dropping methods
VALID_DROPMETHODS = [
    None,  # no dropping
    'threshold',  # drop values below threshold
    'npeaks',  # keep top n number of peaks
    # 'consolidate',  # consolidate intensities
]

# valid grouping methods
VALID_GROUP_METHODS = [
    'weighted',
    'centroid',
]


def bar_isotope_pattern(
        rawip: list,
        delta: float = 0.5,
        method: str = 'weighted',
        verbose: bool = VERBOSE,
):
    """
    Converts a raw isotope pattern into a bar isotope pattern. This groups mass defects
    that are within a given difference from each other into a single *m/z* value and
    intensity.

    :param rawip: The raw isotope pattern with no grouping applied
    :param delta: The *m/z* difference to check around a peak when grouping it into a single *m/z* value.
        The script will look delta/2 from the peak being checked
    :param method: Method of combining (weighted or centroid). Weighted is recommended for accuracy
    :param verbose: chatty mode
    :return: bar isotope pattern in ``[[m/z values],[intensity values]]`` format.
    :rtype: list
    """
    if method not in VALID_GROUP_METHODS:
        raise ValueError(f'The grouping method {method} is invalid. Choose from {", ".join(VALID_GROUP_METHODS)}')
    if verbose is True:
        logger.info('generating bar isotope pattern')
    if isinstance(rawip, Spectrum):  # if handed a Spectrum object, trim before continuing
        rawip = rawip.trim()
    groupedip = group_masses(rawip, delta / 2)
    out = [[], []]
    for group in groupedip:
        if method == 'weighted':
            x, y = weighted_average(*group)  # determine weighted mass and summed intensity
        elif method == 'centroid':
            x, y = centroid(group)
        out[0].append(x)
        out[1].append(y)
    maxint = max(out[1])
    for ind, val in enumerate(out[1]):
        out[0][ind] = out[0][ind]  # / abs(charge)
        out[1][ind] = val / maxint * 100.  # normalize to 100
    if verbose is True:
        logger.info('bar isotope pattern generation complete')
    return out
