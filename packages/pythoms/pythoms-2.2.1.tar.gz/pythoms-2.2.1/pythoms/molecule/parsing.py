"""module for parsing molecular formulae"""

from .mass import abbreviations


SIGNS = ['+', '-']  # charge signs
unicode_subscripts = {  # subscripts values for unit representations
    0: f'\u2080',
    1: f'\u2081',
    2: f'\u2082',
    3: f'\u2083',
    4: f'\u2084',
    5: f'\u2085',
    6: f'\u2086',
    7: f'\u2087',
    8: f'\u2088',
    9: f'\u2089',
}
unicode_superscripts = {  # superscript values for unit representations
    0: f'\u2070',
    1: f'\u00b9',
    2: f'\u00b2',
    3: f'\u00b3',
    4: f'\u2074',
    5: f'\u2075',
    6: f'\u2076',
    7: f'\u2077',
    8: f'\u2078',
    9: f'\u2079',
}

# valid start and end brackets
OPENING_BRACKETS = ['(', '{', '[']  # opening brackets
CLOSING_BRACKETS = [')', '}', ']']  # closing brackets


def interpret(block: str):
    """
    Interprets an element block, breaking it into element and number of that element.

    :param block: string block describing an element
    :return: composition dictionary
    :rtype: dict
    """
    if block[0].isdigit() is True:  # if isotope number is encountered
        return {block: 1}
    else:
        ele = block[0]
        i = 0
        num = ''
        while i < len(block) - 1:
            i += 1
            if block[i].isdigit() is True:  # add digits
                num += block[i]
            elif block[i] == ' ':  # ignore spaces
                continue
            else:
                ele += block[i]
        if num == '':
            num = 1
        else:
            num = int(num)
        return {ele: num}


def interpret_charge(string: str):
    """
    Interprets a charge string.

    :param string: string describing the charge (e.g. '2+')
    :return: charge, sign
    :rtype: tuple
    """
    value = ''
    sign = '+'  # default value for sign
    if type(string) is int:
        return string, sign
    for ind, val in enumerate(string):
        if val in SIGNS:  # if val sets mode
            sign = val
        else:  # number
            value += val
    if value == '':  # if no number was specified (e.g. "+")
        value = 1
    return int(value), sign


def to_subscript(number):
    """
    Converts the value to subscript characters.

    :param int number: number to convert
    :return: subscript
    :rtype: str
    """
    return ''.join(
        [unicode_subscripts[int(val)] for val in str(abs(number))]
    )


def to_superscript(val):
    """
    Returns the integer value represented as a superscript string.

    :param int val: value to represent
    :return: superscript string
    :rtype: str
    """
    return ''.join(
        [unicode_superscripts[int(val)] for val in str(abs(val))]
    )


def chew_formula(formula: str):
    """
    Iterates through provided formula, extracting blocks, interpreting the blocks,
    and returning the formula minus the blocks.

    :param formula: string formula
    :return: remaining formula, interpreted block
    :rtype: str, dict
    """
    if formula[0].isupper() is True:  # element is recognized by an uppercase letter
        block = formula[0]  # element block
        for loc in range(len(formula)):
            if loc == 0:
                continue
            if formula[loc].isupper() is True:  # if an uppercase character is encountered
                break
            elif formula[loc] in OPENING_BRACKETS:  # if a bracket is encountered
                break
            else:
                block += formula[loc]
        return formula[len(block):], interpret(block)  # return remaining formula and the interpreted block
    elif formula[0] in OPENING_BRACKETS:  # if a bracket is encountered, intialize bracket interpretation
        return bracket(formula)
    elif formula[0].isdigit() is True:  # either isotope or charge
        if any([sign in formula for sign in SIGNS]):  # if the block is a value-sign charge specification
            return '', {'charge': formula}
        for ind, val in enumerate(formula):
            if formula[ind].isalpha() is True:  # if isotope encountered, return that isotope with n=1
                return '', {formula: 1}
    elif formula[0] in SIGNS:  # charge specification
        return '', {'charge': formula}  # assign as charge for later interpretation
    else:
        raise ValueError(f'An uninterpretable formula chunck was encountered: {formula}')


def bracket(form):
    """finds the string block contained within a bracket and determines the formula within that bracket"""
    bracktype = OPENING_BRACKETS.index(form[0])  # sets bracket type (so close bracket can be identified)
    bnum = ''  # number of things indicated in the bracket
    block = ''  # element block
    nest = 1  # counter for nesting brackets
    for loc in range(len(form)):  # look for close bracket
        if loc == 0:
            continue
        elif form[loc] == OPENING_BRACKETS[bracktype]:  # if a nested bracket is encountered
            nest += 1
            block += form[loc]
        elif form[loc] == CLOSING_BRACKETS[bracktype]:  # if close bracket is encountered
            nest -= 1
            if nest == 0:
                i = loc + 1  # index of close bracket
                break
            else:
                block += form[loc]
        else:
            block += form[loc]

    try:  # look for digits outside of the bracket
        while form[i].isdigit() is True:
            bnum += form[i]
            i += 1
    except IndexError:  # if i extends past the length of the formula
        pass
    except UnboundLocalError:  # if a close bracket was not found, i will not be defined
        raise ValueError(
            f'A close bracket was not encountered for the "{form[0]}" bracket in the formula segment "{form}". '
            f'Please check your input molecular formula.')

    lblock = len(block) + len(
        bnum) + 2  # length of the internal block + the length of the number + 2 for the brackets
    if bnum == '':  # if no number is specified
        bnum = 1
    else:
        bnum = int(bnum)
    outdict = {}
    while len(block) > 0:  # chew through bracket
        ftemp, tempdict = chew_formula(block)
        for key in tempdict:
            try:
                outdict[key] += tempdict[key] * bnum
            except KeyError:
                outdict[key] = tempdict[key] * bnum
        block = ftemp
    return form[lblock:], outdict  # returns remaining formula and composition of the block


def composition_from_formula(formula):
    """
    Interprets a provided string as a molecular formula.
    Supports nested brackets, charges, and isotopes.

    :param formula:  A molecular formula. Charge may be specified in the formula, but care must be taken to specify
        the charge in sign-value format (e.g. '+2' if value-sign is specified, the script will attempt to interpret the
        key as an isotope).
    :return: A dictionary where each key is an element or isotope with its value
        being the number of each of the elements or isotopes. e.g. the
        molecule CH4 would have the composition ``comp = {'C':1, 'H':4}``
    :rtype: dict
    """
    comp = {}
    while len(formula) > 0:  # chew through formula
        ftemp, nomdict = chew_formula(formula)  # find the next block
        for ele in nomdict:
            try:
                comp[ele] += nomdict[ele]
            except KeyError:
                comp[ele] = nomdict[ele]
        formula = ftemp
    comp = abbreviations(comp)  # look for common abbreviations
    return comp
