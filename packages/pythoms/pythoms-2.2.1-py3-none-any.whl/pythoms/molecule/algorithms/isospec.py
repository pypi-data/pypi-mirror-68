from IsoSpecPy import IsoThreshold

from ..settings import THRESHOLD, VERBOSE
from ..mass import mass_dict
from ..logging import logger
from ...spectrum import Spectrum


logger = logger.getChild(__name__)


# flag for reminding folk to cite people
_ISOSPEC_CITATION_REMINDER = False


def isotope_pattern_isospec(
        comp: dict,
        decpl: int,
        verbose: bool = VERBOSE,
        threshold: float = THRESHOLD,
        **kwargs,
):
    """
    Generates a raw isotope pattern using the isospecpy package. http://matteolacki.github.io/IsoSpec/

    :param comp: composition dictionary
    :param decpl: decimal places to track while converting from isospec to Spectrum
    :param verbose: chatty mode
    :param threshold: threshold level (relative, seems slightly buggy)
    :param kwargs: catch for extra kwargs
    :return: Spectrum object
    """
    logger.info('retrieving isotope pattern from isospec')
    global _ISOSPEC_CITATION_REMINDER  # todo make this non-global
    if _ISOSPEC_CITATION_REMINDER is False:  # remind the user on the first use
        print('IsoSpecPy package was used, please cite https://dx.doi.org/10.1021/acs.analchem.6b01459')
        _ISOSPEC_CITATION_REMINDER = True

    if any([key not in mass_dict for key in comp]):
        # todo see if there's a workaround for isotope specification
        raise KeyError(f'Isotope specification is not supported in IsoSpec calling. Please use a different isotope '
                       f'pattern generation method for isotopes. ')

    # todo see if there's a way to use IsoThresholdGenerator instead
    # use IsoSpec algorithm to generate configurations
    iso_spec = IsoThreshold(
        formula="".join(f'{ele}{num}' for ele, num in comp.items()),
        threshold=threshold * 0.1,
    )

    spec = Spectrum(
        decpl,  # decimal places
        start=min(iso_spec.masses) - 10 ** -decpl,  # minimum mass
        end=max(iso_spec.masses) + 10 ** -decpl,  # maximum mass
        empty=True,
        filler=0.  # fill with zeros, not None
    )
    # add values to Spectrum object
    for mass, abund in zip(iso_spec.masses, iso_spec.probs):
        spec.add_value(
            mass,
            abund
        )
    spec.normalize()  # normalize values to 100.
    logger.info('isospec isotope pattern retrieval complete')
    return spec
