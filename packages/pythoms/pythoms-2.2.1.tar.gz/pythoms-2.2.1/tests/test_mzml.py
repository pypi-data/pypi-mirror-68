import unittest
import os
from pythoms.mzml import mzML
from pythoms.mzml.parsing import branch_attributes
from pythoms.mzml.psims import CVParameterSet


class TestmzML(unittest.TestCase):
    def test_mzml(self):
        mzml = mzML(
            os.path.join(os.path.dirname(__file__), 'MultiTest.mzML.gz'),
            verbose=False
        )
        self.assertEqual(  # check that the correct function keys were pulled
            mzml.functions.keys(),
            {1, 3, 4},
        )

        @mzml.foreachchrom
        def testperchrom(chromatogram):
            attr = branch_attributes(chromatogram)
            return attr['id']

        self.assertEqual(  # test chromatogram decorator
            testperchrom(),
            [u'TIC', u'SRM SIC Q1=200 Q3=100 function=2 offset=0']
        )

        @mzml.foreachscan
        def testperspec(spectrum):
            p = CVParameterSet.create_from_branch(spectrum)
            return p["MS:1000016"].value

        self.assertEqual(  # test spectrum decorator
            testperspec(),
            [0.0171000008, 0.135733336, 0.254333347, 0.372983336, 0.491699994, 0.0510833338, 0.169750005,
             0.288383335, 0.407000005, 0.525833309, 0.0847499967, 0.20341666, 0.322033346, 0.440683335]
        )

        self.assertEqual(  # test intensity summing
            sum(mzml.sum_scans()[1]),
            162804754.0
        )

        self.assertEqual(  # test scan indexing
            sum((mzml[2])[1]),
            6742121
        )

        self.assertEqual(  # test time indexing
            sum((mzml[0.01])[1]),
            56270834
        )
