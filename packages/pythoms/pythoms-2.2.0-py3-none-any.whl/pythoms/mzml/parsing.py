import base64
import re
import zlib
import warnings
from typing import Union, Iterable
from xml.etree import ElementTree

import numpy as np

from .psims import CVParameterSet, stringtodigit

# decoding formats for decoding mzML binary data array strings
decode_formats = {
    'MS:1000519': ['<', 'i'],  # signed 32-bit little-endian integer
    # 'MS:1000520':['',''], # [OBSOLETE] Signed 16-bit float
    'MS:1000521': ['<', 'f'],  # 32-bit precision little-endian floating point conforming to IEEE-754
    'MS:1000522': ['<', 'l'],  # Signed 64-bit little-endian integer
    'MS:1000523': ['<', 'd'],  # 64-bit precision little-endian floating point conforming to IEEE-754.
}

# id string parsing for different manufacturers
_waters_id_re = re.compile('function=(?P<fn>\d+)\sprocess=(?P<proc>\d+)\sscan=(?P<scan>\d+)')
_agilent_id_re = re.compile('scanId=(?P<scan>\d+)')


# prefix for xml elements
_xml_element_prefix = '{http://psi.hupo.org/ms/mzml}'


def branch_attributes(branch: ElementTree.Element):
    """
    Pulls all the attributes of an xml.dom.minidom xml branch.
    These are generally things like index, id, etc.

    :param xml.dom.minidom branch: An xml.dom.minidom object.
    :return: A dictionary of attributes with each key being the attribute name and its value being the value of that
        attribute.
    :rtype: dict

    **Notes**

    The script will attempt to convert any values to float or
    integer in order to reduce TypeErrors when trying to use
    the extracted values.
    """
    return {key: stringtodigit(val) for key, val in branch.attrib.items()}


def decodeformat(p: CVParameterSet, speclen: int):
    """
    Determines the decode format from the accession parameter

    :param p: extracted CVParamterSet of the data array
    :param speclen: length of the spectrum (retrievable from the XML file)
    :return: decode format
    :rtype: str
    """
    for key in set(decode_formats) & p.keys():  # find the set combination of the possibilities
        return f'{decode_formats[key][0]}{speclen}{decode_formats[key][1]}'  # create the decode format


def associate_data_type(cv_params: CVParameterSet):
    """
    Associates a parameter set with a numpy data type

    :param cv_params: set of cv parameters associated with a list of values
    :return: numpy data type
    """
    param_map = {
        '523': np.float64,
        '521': np.float32,
        '522': np.int64,
        '519': np.int32,
        '520': np.float16,
    }
    for key, dtype in param_map.items():
        if f'MS:1000{key}' in cv_params:
            return dtype
    raise ValueError('a data type could not be determined from this parameter set')


def gettext(nodelist):
    """gets text from a simple XML object"""
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def spectrum_array(spectrum: ElementTree.Element) -> np.ndarray:
    """
    Extracts and converts binary data to a numpy ndarray.

    :param spectrum: A spectrum branch element. This element is expected to have two child nodes containing
        binaryDataArrays.
    """
    # spectrum length (defined in the spectrum attributes)
    speclen = int(spectrum.attrib.get('defaultArrayLength'))
    out = np.ndarray((2, speclen))
    # iterate over the binary data arrays
    for ind, bda in enumerate(_findall_ele('binaryDataArrayList', 'binaryDataArray', parent=spectrum)):
        p = CVParameterSet.create_from_branch(bda)  # grab cvparameters

        # pull the binary string
        binary_string = _find_ele('binary', parent=bda).text

        # decode the string
        decoded = base64.standard_b64decode(binary_string)

        # if the string is compressed, decompress
        if 'MS:1000574' in p:
            decoded = zlib.decompress(decoded)

        # retrieve the data from buffer with the associated format
        out[ind] = np.frombuffer(
            decoded,
            associate_data_type(p)
        )

    return out


def get_element_units(spectrum: ElementTree.Element):
    """
    Retrieves the units of the provided element. Assumes that the element has binaryDataArrayList and binaryDataArray
    children which each have a unit-type controlled variable.

    :param spectrum: XML spectrum Element
    :return: x and y units corresponding to the spectrum
    """
    units = []
    # iterate over the binary data arrays
    for bda in _findall_ele('binaryDataArrayList', 'binaryDataArray', parent=spectrum):
        p = CVParameterSet.create_from_branch(bda)  # grab cvparameters
        for cv in p:
            if cv.unit is not None:
                units.append(cv.unit)
    return units


def extract_spectrum(spectrum: ElementTree.Element, units: bool = False) -> list:
    """
    Extracts and converts binary data to two lists.

    :param spectrum: A spectrum branch element. This element is expected to have two child nodes containing
        binaryDataArrays.
    :param units: whether to extract the units from the spectrum
    :return:
    """
    warnings.warn(
        'list retrieval is no longer recommended, please refactor your code to use ndarrays and spectrum_array',
        DeprecationWarning,
        stacklevel=2,
    )
    # todo go through all usages and refactor to array handling
    out = spectrum_array(spectrum).tolist()
    if units is not False:  # extends the units onto out
        out.extend(get_element_units(spectrum))
    return out


def fps(element: ElementTree.Element):
    """
    Extracts function #, process #, and scan # from the idstring of a spectrum branch

    :param element: XML element to retrieve from
    :return:
    """
    # pull id string from scan attribute
    idstring = element.attrib['id']
    match = _waters_id_re.match(idstring)
    if match is not None:
        return (
            int(match.group('fn')),
            int(match.group('proc')),
            int(match.group('scan')),
        )
    else:
        # todo create generalized catch
        match = _agilent_id_re.match(idstring)
        return (
            1,
            None,
            int(match.group('scan'))
        )


def scan_properties(parameters: Union[CVParameterSet, ElementTree.Element]):
    """
    Determines the scan properties of the provided spectrum.

    :param parameters: CVParam parameters
    :return:
    """
    """determines the scan properties of the provided spectrum"""
    mstypes = {  # ms accession keys and their respective names (for spectrum identification)
        'MS:1000928': 'calibration spectrum',
        'MS:1000294': 'mass spectrum',
        'MS:1000322': 'charge inversion mass spectrum',
        'MS:1000325': 'constant neutral gain spectrum',
        'MS:1000326': 'constant neutral loss spectrum',
        'MS:1000328': 'e/2 mass spectrum',
        'MS:1000341': 'precursor ion spectrum',
        'MS:1000343': 'product ion spectrum',
        'MS:1000579': 'MS1 spectrum',
        'MS:1000580': 'MSn spectrum',
        'MS:1000581': 'CRM spectrum',
        'MS:1000582': 'SIM spectrum',
        'MS:1000583': 'SRM spectrum',
    }
    othertypes = {  # other accession keys (non-MS)
        'MS:1000620': 'PDA spectrum',
        'MS:1000804': 'electromagnetic radiation spectrum',
        'MS:1000805': 'emission spectrum',
        'MS:1000806': 'absorption spectrum',
    }
    out = {}
    if isinstance(parameters, CVParameterSet):  # handed a cvparam class object (expected)
        p = parameters
    else:  # handed a tree or branch (generate the cvparam class object)
        p = CVParameterSet.create_from_branch(parameters)
    for acc in p.keys() & mstypes.keys():  # check for ms spectrum
        out['acc'] = acc  # accession code
        out['name'] = mstypes[acc]  # name of spectrum
        out['type'] = 'MS'  # it is a mass spectrum
        out['level'] = p['MS:1000511'].value  # ms level
        out['window'] = [p['MS:1000501'].value, p['MS:1000500'].value]  # scan window
        if 'MS:1000129' in p:  # negative scan
            out['mode'] = '-'
        elif 'MS:1000130' in p:  # positive scan
            out['mode'] = '+'
        if 'MS:1000827' in p:  # if there is an isolation window target m/z
            out['target'] = p['MS:1000827'].value
        # if MSn > 2, not sure how to handle this (will have to be hard coded later as I have no examples)
        elif out['level'] > 2:
            raise ValueError(
                'This script has not been coded to handle MSn > 2, please contact the author of the class')
        return out

    for acc in p.keys() & othertypes.keys():  # if the scan is something else
        out['acc'] = acc  # accession code
        out['name'] = othertypes[acc]  # name of spectrum
        if 'MS:1000804' in p:  # if it is a UV-Vis
            out['type'] = 'UV'
        else:  # other other type (not handled by script)
            raise KeyError(
                'The script has not been coded to handle spectra types other than MS and UV-Vis. '
                'Please contact the authors to get this functionality included.')
        return out


def _find_ele(*paths, parent: ElementTree.Element = None) -> ElementTree.Element:
    """
    Performs a find on the element tree.

    Each element name must be prefixed by "{http://psi.hupo.org/ms/mzml}", so this function saves that step.

    :param paths: path names
    :param parent: parent to search (if not provided, root will be used)
    :return: element tree at location
    """
    return parent.find(
        "/".join([
            f'{_xml_element_prefix}{path}' for path in paths
        ])
    )


def _findall_ele(*paths, parent: ElementTree.Element = None) -> Iterable[ElementTree.Element]:
    """
    Performs a findall on the element tree.

    Each element name must be prefixed by "{http://psi.hupo.org/ms/mzml}", so this function saves that step.

    :param paths: path names
    :param parent: parent to search (if not provided, root will be used)
    :return: element tree at location
    """
    return parent.findall(
        "/".join([
            f'{_xml_element_prefix}{path}' for path in paths
        ])
    )
