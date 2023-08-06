import os
import pathlib
import subprocess
import sys

from .logging import logger


def file_present(filepath):
    """checks for the presence of the specified file or directory in the current working directory"""
    tf = os.path.isfile(filepath)  # look for file first
    if tf is False:  # if file cannot be found, look for directory
        tf = os.path.isdir(filepath)
    return tf


def pw_convert(filename,
               bit=64,
               compression=True,
               gzip=True,
               verbose=True,
               out_directory=None
               ):
    """
    Runs msconvert.exe from ProteoWizard to convert Waters .RAW format to .mzXML
    which can then be parsed by python.

    module requirements: os, subprocess, sys

    ProteoWizard must be installed for this script to function.
    go to
    http://proteowizard.sourceforge.net/downloads.shtml
    to download

    This script assumes that the ProteoWizard is installed under either
    c:\\program files\\proteowizard
    or
    c:\\program files (x86)\\proteowizard

    If you use this python script to convert to mzML, you should cite the paper of the folks who wrote the program
    Chambers, M.C. Nature Biotechnology 2012, 30, 918-920
    doi 10.1038/nbt.2377

    :param filename: file name to convert
    :param bit: floating point bit precision (32 or 64)
    :param compression: enable zlib compression of data in output file (saves space but increases processing time)
    :param gzip: enable gzip compression of output file (saves disk space but increases processing time)
    :param verbose: verbose for subprocess call
    :param out_directory: optional output directory (if not specified, the file will be saved to the same directory as
        the data)
    :return: the file path for the generated file
    """

    def find_all(fname, path):
        """
        Finds all files of a given name within a specified directory.
        Adapted from http://stackoverflow.com/questions/1724693/find-a-file-in-python

        Module dependancies: os
        """
        locations = []
        for root, dirs, files in os.walk(path):
            if fname in files:
                locations.append(os.path.join(root, fname))
        return locations

    if sys.platform != 'win32':
        raise OSError(
            'The function that converts to mzML is limited to Windows operating systems.\n'
            'You can manually convert to *.mzML using the proteowizard standalone package '
            'and supply that mzML file to this script')
    locs = []
    for val in ['c:\\program files\\proteowizard',
                'c:\\program files (x86)\\proteowizard']:  # searches for msconvert.exe in expected folders
        locs.extend(find_all('msconvert.exe', val))

    if len(locs) == 0:  # if script cannot find msconvert.exe
        raise IOError(
            'The python script could not find msconvert.exe\n'
            'Please ensure that ProteoWizard is installed in either:\n'
            'c:\\program files\\proteowizard\nor\nc:\\program files (x86)\\proteowizard')

    filename = pathlib.Path(filename)
    if out_directory is None:
        out_directory = filename.parent

    if bit not in [32, 64]:
        raise ValueError(
            f'an invalid floating point precision was specified"{bit}".')

    callstring = " ".join([
        f'{locs[-1]} "{filename}"',  # main call
        f'-o "{out_directory}"',  # output directory
        '--mzML',
        '--gzip' if gzip else '',  # gzip compression
        '--zlib' if compression else '',  # zlib compression
        f'--{bit}',  # floating point precision
        '--verbose' if verbose else '',  # verbose mode
    ])

    out_exten = f'.mzML{".gz" if gzip else ""}'

    logger.info(f'Generating mzML file from {filename}')
    subprocess.call(callstring)
    logger.info('conversion DONE')
    filename.with_suffix(f'.mzML{".gz" if gzip else ""}')


def fix_extension(fn):
    """tries to fix invalid file extensions"""
    oopsx = {'.mzm': 'l', '.mz': 'ml', '.m': 'zml', '.': 'mzml'}  # incomplete mzml extensions
    oopsr = {'.ra': 'w', '.r': 'aw', '.': 'raw'}  # incomplete raw extionsions
    oopsg = {'.mzml.g': 'z', '.mzml.': 'gz', '.mzml': '.gz', '.mzm': 'l.gz', '.mz': 'ml.gz', '.m': 'zml.gz',
             '.': 'mzml.gz'}  # incomplete gz extensions
    # looks for missing extensions first
    if file_present(fn + '.mzml.gz') is True:
        return fn + '.mzml.gz'
    if file_present(fn + '.mzml') is True:
        return fn + '.mzml'
    for key in oopsg:  # tries to complete mzml.gz shortenings
        if fn.lower().endswith(key) is True:
            if file_present(fn + oopsg[key]) is True:
                return fn + oopsg[key]
    for key in oopsx:  # tries to complete mzml shortenings
        if fn.lower().endswith(key) is True:
            if file_present(fn + oopsx[key]) is True:
                return fn + oopsx[key]
    for key in oopsr:  # tries to complete raw shortenings
        if fn.lower().endswith(key) is True:
            if file_present(fn + oopsr[key]) is True:
                return fn + oopsr[key]
    if file_present(fn + '.raw') is True:  # finally looks for raw file
        return fn + '.raw'
    raise FileNotFoundError(f'The file {fn} could not be located in the current working directory')