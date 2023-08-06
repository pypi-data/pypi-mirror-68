import os
import importlib.util

from ._mass_abbreviations import abbrvs
from . import _mass_dictionaries

"""Mass dictionary associated with the instance"""
MASS_KEY = 'crc_mass'
mass_dict = getattr(
    _mass_dictionaries,
    MASS_KEY,
)

# attempt to load abbreviation dictionary from current working directory
try:
    abbrv_spec = importlib.util.spec_from_file_location(
        'user_abbrvs',
        os.path.join(
            os.getcwd(),
            'user_mass_abbreviations.py'
        )
    )
    abbrv_module = importlib.util.module_from_spec(abbrv_spec)
    abbrv_spec.loader.exec_module(abbrv_module)
    user_abbrvs = abbrv_module.user_abbrvs
    abbrvs.update(user_abbrvs)
except FileNotFoundError:  # if it can't find the file, continue with default abbreviations
    pass


def element_intensity_list(element: str):
    """
    Returns the non-zero element intensity for the specified element.

    :param element: element key
    :return: mass, intensity lists
    :rtype: list
    """
    if element not in mass_dict:
        raise KeyError(f'The element {element} is not defined in the mass dictionary.')
    ele_dict = mass_dict[element]
    mass_out = []
    intensity_out = []
    for isotope in ele_dict:
        if isotope != 0 and ele_dict[isotope][1] != 0.:
            mass_out.append(ele_dict[isotope][0])
            intensity_out.append(ele_dict[isotope][1])
    return [mass_out, intensity_out]


def string_to_isotope(string: str):
    """
    Attempts to interpret an undefined key as an isotope/element combination (e.g. "13C" becomes 'C', 13). Raises a
    ValueError if the string cannot be interpreted as such.

    :param string: string to interpret
    :return: element, isotope
    :rtype: (str, int)
    """
    iso = string[0]
    if iso.isdigit() is False:
        raise TypeError(f'The isotope "{string}" is not a valid format. Use isotope/element format e.g. "12C"')
    ele = ''
    i = 1
    try:
        while i < len(string):
            if string[i].isdigit() is True:
                iso += string[i]
                i += 1
            if string[i].isalpha() is True:
                ele += string[i]
                i += 1
        return ele, int(iso)
    except ValueError:
        raise ValueError(
            f'The string "{string}" could not be interpreted as an element, isotope combination, please check'
            f'your input')


def check_in_mass_dict(comp: dict):
    """
    Checks for the presence of the dictionary keys in the mass dictionary. Raises a ValueError if the key is not found.

    :param comp: composition dictionary
    """
    for key in comp:
        if key not in mass_dict:
            ele, iso = string_to_isotope(key)
            if ele not in mass_dict:
                raise ValueError(f'The element {ele} is not defined in the mass dictionary. Please check your input.')
            elif iso not in mass_dict[ele]:
                raise ValueError(
                    f'The element "{ele}" does not have a defined isotope "{iso}" in the mass dictionary. '
                    f'Please check your input.'
                )


def abbreviations(dct: dict):
    """
    Searches for abbreviations predefined in _mass_abbreviations.py either in the pythoms package or in the current
    working directory. Any found abbreviations will be added to the current dictionary.

    :param dct: incoming dictionary
    :return: un-abbreviated dictionary
    :rtype: dict
    """
    comptemp = {}
    for key in dct:
        if key in abbrvs:  # if a common abbreviation is found in formula
            for subkey in abbrvs[key]:
                try:
                    comptemp[subkey] += abbrvs[key][subkey] * dct[key]
                except KeyError:
                    comptemp[subkey] = abbrvs[key][subkey] * dct[key]
        else:
            try:
                comptemp[key] += dct[key]
            except KeyError:
                comptemp[key] = dct[key]
    return comptemp
