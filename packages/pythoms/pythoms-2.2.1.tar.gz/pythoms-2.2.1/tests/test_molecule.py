import unittest

from pythoms.molecule import Molecule, IPMolecule
from pythoms.molecule.algorithms import VALID_DROPMETHODS, VALID_IPMETHODS


class TestMolecule(unittest.TestCase):
    def setUp(self):
        self.mol = Molecule('L2PdAr+I')
        self.ipmol = IPMolecule(
            'L2PdAr+I',
            ipmethod='multiplicative',
            dropmethod='threshold',
            threshold=0.01,
        )

    def test_molecule(self):
        self.assertEqual(
            self.mol.molecular_formula,
            'C61H51IP3Pd'
        )
        self.assertEqual(
            self.mol.composition,
            {'C': 61, 'H': 51, 'P': 3, 'Pd': 1, 'I': 1}
        )
        self.assertEqual(
            self.mol.molecular_weight,
            1110.300954404405
        )
        self.assertEqual(
            self.mol.monoisotopic_mass,
            1109.12832
        )

    def test_ipmolecule_methods(self):
        for ipmethod in VALID_IPMETHODS:
            for dropmethod in VALID_DROPMETHODS:
                mol = IPMolecule(
                    'Pd2C10H5',
                    ipmethod=ipmethod,
                    dropmethod=dropmethod,
                )
                test = mol.gaussian_isotope_pattern  # test gaussian isotope pattern generation

    def test_ipmolecule(self):
        self.assertEqual(
            self.ipmol.estimated_exact_mass,
            1109.1303706381723,
        )
        self.assertEqual(
            self.ipmol.barip,
            [[1105.130443, 1106.133823749481, 1107.1290292337153, 1108.1305157201678, 1109.1303706381723,
              1110.1328590930914, 1111.1301978511672, 1112.1325950611867, 1113.1318575059308, 1114.134086933976,
              1115.1370272665604, 1116.140052, 1117.143407],
             [2.287794397621507, 1.5228133756325326, 25.476059354316945, 66.8193866193291, 100.0, 52.65050639843156,
              74.88108058795096, 42.5730473226288, 39.36707265932168, 20.17253048748261, 5.990476280101723,
              1.1848920932846654, 0.16082254122736006]]
        )
        self.ipmol - 'PPh3'  # test subtraction
        self.ipmol + 'PPh3'  # test addition
        mol2 = IPMolecule(
            'N(Et)2(CH2(13C)H2(2H))2',
            ipmethod='multiplicative',
        )
        mol2 + self.ipmol  # test class addition
