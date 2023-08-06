import copy

import numpy as np

from .settings import VERBOSE
from .logging import logger
from .parsing import interpret_charge, composition_from_formula, to_subscript, to_superscript
from .mass import abbreviations, check_in_mass_dict, mass_dict, string_to_isotope


class Molecule(object):
    _comp = {}  # storage for composition of the molecule
    _mf = ''
    verbose = VERBOSE

    def __init__(self,
                 string: (str, dict),
                 charge=1,
                 mass_key='nist_mass',
                 verbose=False,
                 ):
        """
        Calculates many properties of a specified molecule.

        :param str, dict string: The molecule to interpret. A composition dictionary may also be specified here.
        :param int, str charge: the charge of the molecule (for mass spectrometric applications).
            This will affect any properties related to the mass to charge
            ratio. If the charge is specified in the input molecular formula, this will be
            overridden.
        :param str mass_key: The mass dictionary to use for calculations. Default is nist_mass, but additional mass
            dictionaries may be defined in the mass_dictionary file and retrieved using the dictionary name
            used to define them.
        :param bool verbose: Verbose output. Mostly useful when calculating for large molecules or while debugging.

        **Notes regarding string specification**

        - Common abbreviations may be predefined in _mass_abbreviations.py (either locally or in the current working
            directory)

        - Use brackets to signify multiples of a given component (nested brackets are supported)

        - Isotopes may be specified using an isotope-element format within a bracket (e.g. carbon 13 would be specified
            as "(13C)" ). The mass of that isotope must be defined in the mass dictionary being used by the script
            (default NIST mass).

        - The charge may be specified in the formula, but care must be taken here. Charge must be specified in either
            sign-value (e.g. '+2') or within a bracket. Otherwise, the script may attempt to interpret the charge as a
            magnitude specifier of the previous block or as an isotope, and errors will be encountered.

        - A composition dictionary with the format `{'Element': number_of_that_element, ...}` may be provided instead
            of a string formula

        """
        logger.debug(f'generating {self.__class__.__name__} object from input {string}')
        # split charge into value and sign
        self.charge, self.sign = interpret_charge(charge)
        self.mass_key = mass_key  # store mass dictionary that the script will use
        self.verbose = verbose
        if type(string) == dict:  # if a composition dictionary was provided
            self.composition = string
        elif type(string) == str:  # set string and interpret formula
            self.molecular_formula = string
        else:
            raise TypeError(f'The provided string type is not interpretable: {type(string)}')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.molecular_formula})'

    def __str__(self):
        return self.__repr__()

    def __contains__(self, item):
        if type(item) == str:
            return item in self._comp
        elif type(item) == list or type(item) == tuple:
            return all([element in self._comp for element in item])
        elif type(item) == dict:
            return all([
                element in self._comp and self._comp[element] >= num for element, num in item.items()
            ])
        elif isinstance(item, Molecule):
            return self.__contains__(item.composition)
        else:
            raise TypeError(f'The item {item} is not a recognized type for containment checks. Type: {type(item)}')

    def __iter__(self):
        for element in self._comp:
            yield element

    def __getitem__(self, item):
        return self._comp[item]

    def __eq__(self, other):
        if type(other) == dict:
            return other == self._comp
        elif isinstance(other, Molecule):
            return other.composition == self._comp
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if type(other) == dict:
            return all([
                number < self._comp[element] for element, number in other.items()
            ])
        elif isinstance(other, Molecule):
            return all([
                number < self._comp[element] for element, number in other.composition.items()
            ])
        else:
            raise TypeError(f'Comparison of type {type(other)} to {self.__class__} is unsupported. ')

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        if type(other) == dict:
            return all([
                number > self._comp[element] for element, number in other.items()
            ])
        elif isinstance(other, Molecule):
            return all([
                number > self._comp[element] for element, number in other.composition.items()
            ])
        else:
            raise TypeError(f'Comparison to type {type(other)} to {self.__class__} is unsupported. ')

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __getinitargs__(self):
        return (
            self.composition,
            f'{self.charge}{self.sign}',
            self.mass_key,
            self.verbose,
        )

    def _get_kwargs(self) -> dict:
        """gets the kwargs associated with the instance for reinstantiation"""
        return {
            'charge': self.charge,
            'mass_key': self.mass_key,
            'verbose': self.verbose,
        }

    def __reduce__(self):
        """pickle support"""
        return (
            self.__class__,
            self.__getinitargs__(),
        )

    def __add__(self, other):
        """
        Several supported addition methods:
        If a valid molecular formula string is provided, that string will be added.
        If another Molecule class instance is provided, the provided instance will be
        added to the current instance.
        """
        if type(other) is str:
            other = composition_from_formula(other)
        elif isinstance(other, Molecule) is True:
            other = other.composition
        elif type(other) == dict:
            pass
        else:
            raise ValueError(f'Addition of {other} to {self} is invalid')
        new = copy.copy(self._comp)  # starter for new dictionary

        for key in other:
            try:
                new[key] += other[key]
            except KeyError:
                new[key] = other[key]
        return self.__class__(
            new,
            **self._get_kwargs(),
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if type(other) is str:
            other = composition_from_formula(other)
        elif isinstance(other, Molecule) is True:
            other = other.composition
        elif type(other) == dict:
            pass
        else:
            raise ValueError(f'Addition of {other} to {self} is invalid')
        new = copy.copy(self._comp)  # starter for new dictionary
        for key in other:
            try:
                new[key] += other[key]
            except KeyError:
                new[key] = other[key]
        self.composition = new
        return self

    def __sub__(self, other):
        """
        See __add__ for details.
        Subtract has a catch for a negative number of a given element
        (the minimum that can be reached is zero).
        """
        if type(other) is str:
            other = composition_from_formula(other)
        elif isinstance(other, Molecule) is True:
            other = other.composition
        elif type(other) == dict:
            pass
        else:
            raise ValueError(f'Addition of {other} to {self} is invalid')
        new = copy.copy(self._comp)  # starter for new dictionary

        for key in other:
            if new[key] - other[key] < 0 or key not in new:
                raise ValueError('Subtraction of {other[key]} {key} from {self} would yield a negative number of that '
                                 'element.')
            new[key] -= other[key]
        return self.__class__(
            new,
            **self._get_kwargs(),
        )

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        if type(other) is str:
            other = composition_from_formula(other)
        elif isinstance(other, Molecule) is True:
            other = other.composition
        elif type(other) == dict:
            pass
        else:
            raise ValueError(f'Addition of {other} to {self} is invalid')
        new = copy.copy(self._comp)  # starter for new dictionary

        for key in other:
            if new[key] - other[key] < 0 or key not in new:
                raise ValueError('Subtraction of {other[key]} {key} from {self} would yield a negative number of that '
                                 'element.')
            new[key] -= other[key]
        self.composition = new
        return self

    def __mul__(self, other):
        """allows integer multiplication of the molecular formula"""
        if type(other) != int:
            raise ValueError(f'Non-integer multiplication of a {self.__class__.__name__} object is unsupported')
        new = copy.copy(self._comp)  # starter for new dictionary
        for key in new:
            new[key] = new[key] * other
        return self.__class__(
            new,
            **self._get_kwargs(),
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        if type(other) != int:
            raise ValueError(f'Non-integer multiplication of a {self.__class__.__name__} object is unsupported')
        new = copy.copy(self._comp)  # starter for new dictionary
        for key in new:
            new[key] = new[key] * other
        self.composition = new
        return self

    def __truediv__(self, other):
        """allows integer division of the molecular formula"""
        if type(other) != int:
            raise ValueError(f'Non-integer division of a {self.__class__.__name__} object is unsupported')
        new = copy.copy(self._comp)  # starter for new dictionary
        for key in new:
            newval = new[key] / other
            if newval.is_integer() is False:
                raise ValueError(f'Division of {new[key]} {key} by {other} yielded a non-integer number {newval}')
            new[key] = int(newval)
        return self.__class__(
            new,
            **self._get_kwargs(),
        )

    def __itruediv__(self, other):
        if type(other) != int:
            raise ValueError(f'Non-integer division of a {self.__class__.__name__} object is unsupported')
        new = copy.copy(self._comp)  # starter for new dictionary
        for key in new:
            newval = new[key] / other
            if newval.is_integer() is False:
                raise ValueError(f'Division of {new[key]} {key} by {other} yielded a non-integer number {newval}')
            new[key] = int(newval)
        self.composition = new
        return self

    @property
    def composition(self):
        """Composition dictionary"""
        return self._comp

    @composition.setter
    def composition(self, dct):
        if type(dct) != dict:
            raise TypeError('The composition must be a dictionary')
        dct = copy.copy(dct)
        dct = abbreviations(dct)  # check for and convert abbreviations
        if 'charge' in dct:  # if charge was specified in the formula
            self.charge, self.sign = interpret_charge(dct['charge'])
            del dct['charge']
        check_in_mass_dict(dct)  # check in mass dictionary
        self._comp = dct  # set local dictionary

    @property
    def molecular_formula(self):
        """Molecular formula of the molecule"""
        out = ''
        # todo catch carbon and hydrogen isotopes first
        if 'C' in self.composition:  # carbon and hydrogen first according to hill formula
            out += f'C{self.composition["C"]}' if self.composition['C'] > 1 else 'C'
        if 'H' in self.composition:
            out += f'H{self.composition["H"]}' if self.composition['H'] > 1 else 'H'
        for key, val in sorted(self.composition.items()):  # alphabetically otherwise
            if key != 'C' and key != 'H':
                if key in mass_dict:
                    out += f'{key}{self.composition[key]}' if self.composition[key] > 1 else f'{key}'
                else:  # if an isotope
                    ele, iso = string_to_isotope(key)
                    out += f'({iso}{ele})'
                    out += f'{self.composition[key]}' if self.composition[key] > 1 else ''
        return out

    @molecular_formula.setter
    def molecular_formula(self, formula):
        self.composition = composition_from_formula(formula)
        self._mf = formula

    @property
    def molecular_formula_formatted(self):
        """returns the subscript-formatted molecular formula"""
        out = ''
        if 'C' in self.composition:
            out += f'C{to_subscript(self.composition["C"]) if self.composition["C"] > 1 else "C"}'
        if 'H' in self.composition:
            out += f'H{to_subscript(self.composition["H"]) if self.composition["H"] > 1 else "H"}'
        for key, val in sorted(self.composition.items()):
            if key not in ['C', 'H']:
                if key in mass_dict:
                    out += f'{key}{to_subscript(self.composition[key])}' if self.composition[key] > 1 else f'{key}'
                else:
                    ele, iso = string_to_isotope(key)
                    out += f'{to_superscript(iso)}{ele}'
                    out += f'{to_subscript(self.composition[key])}' if self.composition[key] > 1 else ''
        return out

    @property
    def sf(self):
        """legacy catch for shorthand 'string formula' attribute"""
        return self.molecular_formula

    @property
    def molecular_weight(self):
        """Molecular weight of the molecule"""
        mwout = 0
        for element, number in self.composition.items():
            try:
                mass = mass_dict[element]
                for isotope in mass:
                    if isotope == 0:
                        continue
                    # add every isotope times its natural abundance times the number of that element
                    mwout += mass[isotope][0] * mass[isotope][1] * number
            except KeyError:  # if isotope
                ele, iso = string_to_isotope(element)
                mwout += mass_dict[ele][iso][0] * number  # assumes 100% abundance if specified
        return mwout

    @property
    def mw(self):
        """legacy catch for shorthand molecular weight"""
        return self.molecular_weight

    @property
    def percent_composition(self):
        """Elemental percent composition of the molecule"""
        pcompout = {}  # percent composition dictionary
        for element, number in self.composition.items():
            try:
                mass = mass_dict[element]
                for isotope in mass:
                    if isotope == 0:
                        continue
                    if element not in pcompout:
                        pcompout[element] = 0.
                    # add mass contributed by that element
                    pcompout[element] += mass[isotope][0] * mass[isotope][1] * number
            except KeyError:  # if isotope
                ele, iso = string_to_isotope(element)
                pcompout[str(iso) + ele] = mass_dict[ele][iso][0] * number
        mw = self.molecular_weight
        for element in pcompout:  # determines the percent composition of each element
            try:
                pcompout[element] = pcompout[element] / mw
            except ZeroDivisionError:
                pcompout[element] = 0.
        return pcompout

    @property
    def pcomp(self):
        """legacy catch for shorthand percent composition"""
        return self.percent_composition

    @property
    def monoisotopic_mass(self):
        """An estimation of the exact mass given by the molecular formula. This is likely not accurate for high-mass
        species"""
        em = 0.
        for element, number in self.composition.items():
            try:
                em += mass_dict[element][0][0] * number
            except KeyError:
                ele, iso = string_to_isotope(element)
                em += mass_dict[ele][iso][0] * number
        # # accounts for the mass of an electron (uncomment if this affects your data)
        # if self.sign == '+':
        #    em -= (9.10938356*10**-28)*charge
        # if self.sign == '-':
        #    em += (9.10938356*10**-28)*charge
        return em / self.charge

    @property
    def standard_deviation_comp(self):
        """
        cacluates the standard deviation of the isotope pattern of the supplied composition
        this calculation is based on Rockwood and Van Orden 1996 doi: 10.1021/ac951158i
        """
        stdev = 0.
        for element, number in self.composition.items():
            meanmass = 0
            eledev = 0  # elemental deviation
            mass = mass_dict[element]
            for isotope in mass:  # calculate weighted average mass
                if isotope != 0:
                    meanmass += sum(mass[isotope])  # weighted average mass
            for isotope in mass:
                if mass != 0:
                    eledev += mass[isotope][1] * (mass[isotope][0] - meanmass) ** 2
            stdev += eledev * number
        return np.sqrt(stdev)

    def print_details(self):
        """prints the details of the generated molecule"""
        print(f'{self}')
        print(f'formula: {self.molecular_formula}')
        print(f'molecular weight: {round(self.molecular_weight, 6)}')
        print(f'monoisotopic mass: {round(self.monoisotopic_mass, 6)}')
        print('')
        self.print_percent_composition()

    def print_percent_composition(self):
        """prints the percent composition in a reader-friendly format"""
        print('elemental percent composition:')
        for element, percent in sorted(self.percent_composition.items()):
            print(f'{element}: {percent * 100.:6.4}%')
