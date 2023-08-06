from tqdm import tqdm

from ...spectrum import Spectrum
from ..settings import THRESHOLD, NPEAKS, CONSOLIDATE, VERBOSE
from ..logging import logger
from ..util import autodec, numberofcwr, product, num_permu, ReiterableCWR
from ..mass import mass_dict, string_to_isotope


logger = logger.getChild(__name__)


def isotope_pattern_hybrid(composition: dict,
                           fwhm: float,
                           decpl: int,
                           verbose: bool = VERBOSE,
                           dropmethod: str = None,
                           threshold: float = THRESHOLD,
                           npeaks: int = NPEAKS,
                           consolidate: float = CONSOLIDATE,
                           **kwargs,
                           ):
    """
    A hybrid isotope pattern calculator which calculates the isotope pattern from each element, then multiplies the
    lists.

    :param composition: composition dictionary
    :param fwhm: full-width-at-half-maximum
    :param decpl: decimal places to track in the Spectrum object
    :param verbose: chatty mode
    :param dropmethod: optional method to use for low-intensity peak dropping or consolidation. Valid options are
        'threshold', 'npeaks', or 'consolidate'.
    :param threshold: if the dropmethod is set to 'threshold', any peaks below this threshold will be dropped.
    :param npeaks: if the dropmethod is set to 'npeaks', the top n peaks will be kept, with the rest being dropped.
    :param consolidate: if the dropmethod is set to 'consolidate', any peaks below the threshold will be consolidated
        into adjacent peaks using a weighted average. Any peaks that do not have a neighbour within 10^-`consolidate`
        will be dropped entirely.
    :return: isotope pattern as a Spectrum object
    :rtype: Spectrum
    """
    logger.info('generating hybrid isotope pattern')
    eleips = {}  # dictionary for storing the isotope patterns of each element
    for element, number in composition.items():
        eleips[element] = isotope_pattern_combinatoric(  # calculate the isotope pattern for each element
            {element: number},
            decpl=decpl,
            verbose=verbose,
        ).trim()  # trim the generated spectra to lists

    sortlist = []
    for element in eleips:
        sortlist.append((
            len(eleips[element][0]),
            element
        ))
    sortlist = sorted(sortlist)  # sorted list of elements based on the length of their isotope patterns
    sortlist.reverse()

    spec = None
    # todo convert to context tqdm (update string)
    for lenlist, element in tqdm(sortlist, desc='adding element to isotope pattern', disable=not verbose):
        if spec is None:
            spec = Spectrum(
                autodec(fwhm),  # decimal places
                start=None,  # minimum mass
                end=None,  # maximum mass
                empty=True,  # whether or not to use emptyspec
                filler=0.,  # fill with zeros, not None
                specin=eleips[element],  # supply masses and abundances as initialization spectrum
            )
            continue
        spec.add_element(eleips[element][0], eleips[element][1])
        spec.normalize(100.)  # normalize spectrum object
        if dropmethod == 'threshold':  # drop values below threshold
            spec.threshold(threshold)
        elif dropmethod == 'npeaks':  # keep top n number of peaks
            spec.keep_top_n(npeaks)
        elif dropmethod == 'consolidate':  # consolidate values being dropped
            spec.consolidate(
                threshold,
                3 * 10 ** -consolidate
            )
    logger.info('hybrid isotope pattern generation complete')
    return spec


def isotope_pattern_combinatoric(
        comp: dict,
        decpl: int,
        verbose: bool = VERBOSE,
        **kwargs,  # catch for extra keyword arguments
):
    """
    Calculates the raw isotope pattern of a given molecular formula with mass defects preserved.
    Uses a combinatorial method to generate isotope formulae

    :param comp: composition dictionary
    :param decpl: decimal places to track in the Spectrum object
    :param verbose: chatty mode
    :return: raw isotope pattern as a Spectrum object
    :rtype: Spectrum
    """
    logger.info('generating combinatoric isotope pattern')
    speciso = False  # set state for specific isotope
    isos = {}  # isotopes dictionary
    isosets = {}  # set of isotopes for each element
    iterators = []  # list of iterators
    nk = []
    for element in comp:  # for each element
        if element in mass_dict:
            isosets[element] = []  # set of isotopes
            for isotope in mass_dict[element]:  # for each isotope of that element in the mass dictionary
                if isotope != 0 and mass_dict[element][isotope][1] != 0:  # of the intensity is nonzero
                    isosets[element].append(isotope)  # track set of isotopes
                    isos[isotope] = element  # create isotope,element association for reference
            iterators.append(
                ReiterableCWR(  # create iterator instance
                    isosets[element],
                    comp[element]
                )
            )
            if verbose is True:
                nk.append([  # track n and k for list length output
                    len(isosets[element]),
                    comp[element]
                ])
        else:  # if it's an isotope
            speciso = True

    spec = Spectrum(  # initiate spectrum object
        decpl,  # decimal places
        start=None,  # no minimum mass
        end=None,  # no maximum mass
        empty=True,  # whether or not to use emptyspec
        filler=0.,  # fill with zeros, not None
    )

    iterations = int(cpu_list_product([numberofcwr(n, k) for n, k in nk]))  # number of iterations

    for comb in tqdm(product(*iterators), desc='processing isotope combination', total=iterations, disable=not verbose):
        num = 1  # number of combinations counter
        x = 0.  # mass value
        y = 1.  # intensity value
        for tup in comb:  # for each element combination
            element = isos[tup[0]]  # associate isotope to element
            # counts = [tup.count(x) for x in isosets[element]] # count the number of occurances of each isotope
            # num *= num_permu(tup,counts) # determine the number of permutations of the set
            # for ind,isotope in enumerate(isosets[element]):
            #    x += self.md[element][isotope][0] * counts[ind]
            #    y *= self.md[element][isotope][1] ** counts[ind]
            num *= num_permu(tup, isosets[element])  # multiply the number by the possible permutations
            for isotope in tup:  # for each isotope
                x += mass_dict[element][isotope][0]  # shift x
                y *= mass_dict[element][isotope][1]  # multiply intensity
        # add the x and y combination factored by the number of times that combination will occur
        spec.add_value(x, y * num)

    if speciso is True:  # if an isotope was specified
        for element in comp:
            if element not in mass_dict:  # if an isotope
                ele, iso = string_to_isotope(element)  # determine element and isotope
                spec.shift_x(mass_dict[ele][iso][0] * comp[element])  # shift the x values by the isotopic mass
    spec.normalize()  # normalize the spectrum object
    logger.info('combinatoric isotope pattern generation complete')
    return spec


def cpu_list_product(iterable):
    """returns the product of a list"""
    prod = 1
    for n in iterable:
        prod *= n
    return prod
