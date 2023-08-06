import unittest
from random import random

from pythoms.molecule.mass import element_intensity_list
from pythoms.spectrum import Spectrum


class TestSpectrum(unittest.TestCase):
    def test_spectrum(self):
        spec = Spectrum(3)
        spec.add_value(479.1, 1000)
        self.assertEqual(
            spec.trim(),
            [[479.1], [1000]]
        )

        spec2 = Spectrum(3)
        spec2.add_value(443.1, 1000)
        self.assertEqual(
            spec2.trim(),
            [[443.1], [1000]]
        )
        spec += spec2
        self.assertEqual(
            spec.trim(),
            [[443.1, 479.1], [1000, 1000]]
        )
        spec3 = Spectrum(3, start=50, end=2500)
        spec3.add_value(2150.9544, 1000)
        self.assertEqual(
            spec3.trim(),
            [[2150.954], [1000]]
        )
        spec += spec3

        self.assertEqual(
            spec.trim(True),
            [[50.0, 443.1, 479.1, 2150.954, 2500], [0.0, 1000, 1000, 1000, 0.0]]
        )
        spec.end = 2100.
        self.assertEqual(
            spec.trim(),
            [[443.1, 479.1], [1000, 1000]]
        )

    def test_element(self):
        mol = Spectrum(
            3,
            start=0.,
            end=100.,
            filler=0.,
        )
        mol.add_spectrum(  # start with a Cl
            *element_intensity_list('Cl')
        )
        mol.add_element(  # add another Cl
            *element_intensity_list('Cl')
        )
        self.assertEqual(
            mol.trim(),
            [[69.938, 71.935, 73.932], [0.5739577600000001, 0.36728448, 0.05875776]]
        )
        mol.add_element(
            *element_intensity_list('Pd')
        )
        self.assertEqual(
            mol.trim(),
            [[171.843, 173.84, 173.841, 174.842, 175.837, 175.838, 175.841, 176.839, 177.835, 177.838, 177.841, 178.836,
              179.835, 179.838, 179.843, 181.835, 181.84, 183.837],
             [0.005854369152000001, 0.0037463016960000003, 0.06393889446400002, 0.128164767808, 0.000599329152,
              0.040915491072, 0.15686265580800002, 0.082014624384, 0.006545614464, 0.100378848384, 0.15186922329600003,
              0.013120607808, 0.016058495808, 0.097183473408, 0.06726784947200001, 0.015547303296, 0.043045741056,
              0.0068864094719999994]]

        )
        mol.charge = 2
        self.assertEqual(
            mol.trim()[0],
            [85.922, 86.92, 86.921, 87.421, 87.919, 87.919, 87.921, 88.42, 88.918, 88.919, 88.921, 89.418, 89.918,
             89.919, 89.922, 90.918, 90.92, 91.919]

        )
        del mol.charge
        self.assertEqual(
            mol.trim()[0],
            [171.843, 173.84, 173.841, 174.842, 175.837, 175.838, 175.841, 176.839, 177.835, 177.838, 177.841, 178.836,
             179.835, 179.838, 179.843, 181.835, 181.84, 183.837]
        )

    def test_indexing(self):
        """tests calculated indexing for filled Spectrum objects"""
        spec = Spectrum(3, empty=False)
        for i in range(1000):
            num = random()
            mz = num * spec.end
            try:
                index = spec.index(mz)
            except ValueError:
                continue
            self.assertEqual(
                round(mz, 3),
                round(spec.x[index], 3)
            )
