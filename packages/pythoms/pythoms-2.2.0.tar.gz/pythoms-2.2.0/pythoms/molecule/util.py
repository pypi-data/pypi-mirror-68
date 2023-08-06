from itertools import combinations_with_replacement as cwr

import numpy as np
import sympy as sym
from scipy import stats


def standard_deviation(fwhm):
    """determines the standard deviation for a normal distribution with the full width at half max specified"""
    return fwhm / (2 * np.sqrt(2 * np.log(2)))  # based on the equation FWHM = 2*sqrt(2ln2)*sigma


def group_masses(ip, dm: float = 0.25):
    """
    Groups masses in an isotope pattern looking for differences in m/z greater than the specified delta.
    expects

    :param ip: a paired list of [[mz values],[intensity values]]
    :param dm: Delta for looking +/- within
    :return: blocks grouped by central mass
    :rtype: list
    """
    num = 0
    out = [[[], []]]
    for ind, val in enumerate(ip[0]):
        out[num][0].append(ip[0][ind])
        out[num][1].append(ip[1][ind])
        try:
            if ip[0][ind + 1] - ip[0][ind] > dm:
                num += 1
                out.append([[], []])
        except IndexError:
            continue
    return out


def centroid(ipgroup):
    """
    takes a group of mz and intensity values and finds the centroid
    this method results in substantially more error compared to the weighted_average method (~9 orders of
    magnitude for C61H51IP3Pd)
    """
    return sum(ipgroup[0]) / len(ipgroup[0]), sum(ipgroup[1]) / len(ipgroup[1])


def normal_distribution(center, fwhm, height):
    """
    Generates a normal distribution about the center with the full width at half max specified. Y-values will be
    normalized to the height specified.

    :param center: center x value for the distribution
    :param fwhm: full-width-at-half-maximum
    :param height: maximum value for the y list
    :return: x values, y values
    :rtype: list
    """
    x = np.arange(
        center - fwhm * 2,
        center + fwhm * 2,
        10 ** -autodec(fwhm),
        dtype=np.float64,
    )
    y = stats.norm.pdf(  # generate normal distribution
        x,
        float(center),  # type-convert from sympy Float
        standard_deviation(fwhm),
    )
    y /= max(y)  # normalize
    y = y * height
    return [x.tolist(), y.tolist()]


def autodec(fwhm):
    """
    Automatically calculates the appropriate decimal place to track based on a full-width-at-half-maximum

    :param fwhm: full-width-at-half-maximum
    :return: decimal power
    :rtype: int
    """
    shift = fwhm
    n = 0
    while shift < 1.:
        n += 1
        shift = fwhm * 10 ** n
    return n + 1  # track 1 higher


def num_permu(lst, isos):
    """
    Calculates the number of unique permutations of the given set of isotopes for an element.
    The calculation is generated as a sympy function before evaluation. numpy factorial is limited in the size of
    factorials that are calculable, so sympy is required.

    :param lst: list of isotopes in the combination
    :param isos: possible isotopes for that element
    :return: number of occurrences of this list of isotopes
    :rtype: int
    """
    counts = [lst.count(x) for x in isos]  # counts the number of each isotope in the set
    num = sym.factorial(len(lst))  # numerator is the factorial of the length of the list
    denom = 1  # denominator is the product of the factorials of the counts of each isotope in the list
    for count in counts:
        denom *= sym.factorial(count)
    return int((num / denom).evalf())  # divide, evaluate, and return integer


def product(*iterables):
    """
    cartesian product of iterables
    from http://stackoverflow.com/questions/12093364/cartesian-product-of-large-iterators-itertools
    """
    if len(iterables) == 0:
        yield ()
    else:
        it = iterables[0]
        for item in it() if callable(it) else iter(it):
            for items in product(*iterables[1:]):
                yield (item,) + items


def numberofcwr(n, k):
    """
    calculates the number of combinations with repitition
    n: number of things to choose from
    k: choose k of them
    """
    fn = sym.factorial(n + k - 1)
    fn /= sym.factorial(k)
    fn /= sym.factorial(n - 1)
    return fn.evalf()


class ReiterableCWR(object):
    def __init__(self, isos, number):
        """a reiterable version of combinations with replacements iterator"""
        self.isos = isos  # isotopes group
        self.number = number  # number of atoms of the element

    def __iter__(self):
        return cwr(self.isos, self.number)
