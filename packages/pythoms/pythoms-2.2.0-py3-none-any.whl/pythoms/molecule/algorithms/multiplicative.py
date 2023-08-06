from tqdm import tqdm

from ..settings import THRESHOLD, NPEAKS, CONSOLIDATE, VERBOSE
from ..mass import mass_dict, string_to_isotope
from ..logging import logger
from ...spectrum import Spectrum


logger = logger.getChild(__name__)


def isotope_pattern_multiplicative(
        comp: dict,
        decpl: int,
        verbose: bool = VERBOSE,
        dropmethod: str = None,
        threshold: float = THRESHOLD,
        npeaks: int = NPEAKS,
        consolidate: float = CONSOLIDATE,
        **kwargs,
):
    """
    Calculates the raw isotope pattern of a given molecular formula with mass defects preserved.

    :param comp: The molecular composition dictionary. See ``Molecule.composition`` for more details.
    :param decpl: The number of decimal places to track. This is normally controlled by the keyword
        arguments of the class, but can be specified if called separately.
    :param verbose: chatty mode
    :param dropmethod: optional method to use for low-intensity peak dropping or consolidation. Valid options are
        'threshold', 'npeaks', or 'consolidate'.
    :param threshold: if the dropmethod is set to 'threshold', any peaks below this threshold will be dropped.
    :param npeaks: if the dropmethod is set to 'npeaks', the top n peaks will be kept, with the rest being dropped.
    :param consolidate: if the dropmethod is set to 'consolidate', any peaks below the threshold will be consolidated
        into adjacent peaks using a weighted average. Any peaks that do not have a neighbour within 10^-`consolidate`
        will be dropped entirely.
    :return: Returns the isotope pattern with mass defects preserved (referred to as the 'raw'
        isotope pattern in this script).
    :rtype: Spectrum
    """
    spec = None  # initial state of spec
    logger.info('generating multiplicative isotope pattern')

    for key in comp:  # for each element
        if key in mass_dict:  # if not a single isotope
            masses = []  # list for masses of each isotope
            abunds = []  # list for abundances
            for mass in mass_dict[key]:
                if mass != 0:
                    if mass_dict[key][mass][1] > 0:  # if abundance is nonzero
                        masses.append(mass_dict[key][mass][0])
                        abunds.append(mass_dict[key][mass][1])
            msg = f'Processing element {key}'
            for n in tqdm(range(comp[key]), desc=msg, disable=not verbose):  # for n number of each element
                if spec is None:  # if spectrum object has not been defined
                    spec = Spectrum(
                        decpl,  # decimal places
                        start=min(masses) - 10 ** -decpl,  # minimum mass
                        end=max(masses) + 10 ** -decpl,  # maximum mass
                        specin=[masses, abunds],  # supply masses and abundances as initialization spectrum
                        empty=True,  # whether or not to use emptyspec
                        filler=0.,  # fill with zeros, not None
                    )
                    continue
                spec.add_element(masses, abunds)  # add the element to the spectrum object
                spec.normalize(100.)  # normalize spectrum
                if dropmethod == 'threshold':  # drop values below threshold
                    spec.threshold(threshold)
                elif dropmethod == 'npeaks':  # keep top n number of peaks
                    spec.keep_top_n(npeaks)
                elif dropmethod == 'consolidate':  # consolidate values being dropped
                    # todo figure out what's wrong here
                    raise NotImplementedError("There are bugs here, for the time being don't use the 'consolidate' "
                                              "dropmethod.")
                    spec.consolidate(
                        threshold,
                        3 * 10 ** -consolidate
                    )
        else:  # if specific isotope
            ele, iso = string_to_isotope(key)  # find element and isotope
            if spec is None:  # if spectrum object has not been defined
                spec = Spectrum(
                    decpl,  # decimal places
                    start=(mass_dict[ele][iso][0] * float(comp[key])) - 10 ** -decpl,  # minimum mass
                    end=(mass_dict[ele][iso][0] * float(comp[key])) + 10 ** -decpl,  # maximum mass
                    specin=[[mass_dict[ele][iso][0] * float(comp[key])], [1.]],
                    # supply masses and abundances as initialization spectrum
                    empty=True,  # whether or not to use emptyspec
                    filler=0.  # fill with zeros, not None
                )
                continue
            # todo add tqdm progress bar
            spec.shift_x(mass_dict[ele][iso][0])  # offset spectrum object by the mass of that
    spec.normalize()
    logger.info('multiplicative isotope pattern generation complete')
    return spec
