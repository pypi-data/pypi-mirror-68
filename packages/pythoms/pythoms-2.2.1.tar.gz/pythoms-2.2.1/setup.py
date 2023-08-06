from setuptools import setup, find_packages
import pythoms

NAME = 'pythoms'
AUTHOR = 'Lars Yunker'

PACKAGES = find_packages()
KEYWORDS = ', '.join([
    'mass spectrometry',
    'mass spec',
    'mzML',
    'isotope pattern',
    'HUPO PSI-MS',
])

long_description = """
Contains classes and methods for processing mzML files, determining isotope patterns and physicochemical properties, 
and combining spectra of dissimilar shape.
"""

setup(
    name=NAME,
    version=pythoms.__version__,
    description='A Python library to aid in the processing and interpretation of mass spectrometric data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url='https://gitlab.com/larsyunker/PythoMS',
    packages=PACKAGES,
    license='MIT',
    python_requires='~=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Operating System :: OS Independent',
        'Natural Language :: English'
    ],
    install_requires=[
        'numpy>=1.14.2',
        'openpyxl>=2.5.2',
        'matplotlib>=3.2.1',
        'scipy>=1.1.0',
        'sympy>=1.1.1',
        'obonet==0.2.5',  # they changed attribute names without deprecationwarnings, so only this version is verified
        'isospecpy>=2.0.2',
        'tqdm>=4.46.0',
        'packaging>=20.1',
    ],
    package_data={
        '': ['*.obo']
    },
    keywords=KEYWORDS,
)
