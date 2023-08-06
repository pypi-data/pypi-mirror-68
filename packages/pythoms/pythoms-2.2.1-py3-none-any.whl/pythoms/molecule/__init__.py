"""
IGNORE:
Molecule class (previously "isotope pattern generator" and "MolecularFormula")

The output of this builder has been validated against values calculated by ChemCalc (www.chemcalc.org)
Negligable differences are attributed to different low value discarding techniques
(ChemCalc keeps the top 5000 peaks, this script drops values less than a threshold 5 orders of magnitude below the
maximum value)

CHANGELOG:
- added exact mass comparison
- separated fwhm calculation from sigma
- fwhm calculation now uses monoisotopic mass
- barisotope pattern now groups using the full width at half max
- gaussian isotope pattern generation now works off of rawip by default
- updated to use Progress class
- updated gaussian isotope pattern generator to automatically determine the appropriate decimal places
---2.9 INCOMPATIBLE WITH SPECTRUM v2.4 or older
- moved charge application to raw isotope pattern function
- fixed bug in validation function for charged molecules
- added support for and enabled auto-saving of molecule instances (loading and saving to .mol files)
IGNORE
"""

from .base import Molecule
from .ip import IPMolecule
from .logging import logger

__all__ = [
    'Molecule',
    'IPMolecule',
    'logger',
]


if __name__ == '__main__':  # for testing and troubleshooting
    mol = IPMolecule(
        'L2PdAr+I',
        # charge= 2, # specify charge (if not specified in formula)
        # res=1050000, # specify spectrometer resolution (default 5000)
        verbose=True,
        # decpl=10,
        # dropmethod='threshold',
        # threshold=0.00001,
        # ipmethod='hybrid',
        ipmethod='combinatorics',
        # keepall=True,
    )
    mol.print_details()
