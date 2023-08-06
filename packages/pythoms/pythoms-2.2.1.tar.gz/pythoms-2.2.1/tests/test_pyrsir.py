import os
import shutil
import unittest

from pythoms.rsir import RSIR

multitest_xl = os.path.join(os.path.dirname(__file__), 'multitest_pyrsir_validation.xlsx')
multitest_mz = os.path.join(os.path.dirname(__file__), 'MultiTest.mzML.gz')

rxn_xl = os.path.join(os.path.dirname(__file__), 'LY-2015-09-15 06 pyrsir example.xlsx')
rxn_mz = os.path.join(os.path.dirname(__file__), 'LY-2015-09-15 06.mzML.gz')


class TestPyRSIR(unittest.TestCase):
    def test_multitest(self):
        """runs the multitest stage"""
        shutil.copy(
            multitest_xl,
            f'{multitest_xl}.bak'
        )
        try:
            rsir = RSIR(
                multitest_mz,
                bin_numbers=[3, 5],
            )
            rsir.add_targets_from_xlsx(
                multitest_xl,
            )
            rsir.extract_data()
            rsir.write_rsir_to_excel(f'{multitest_xl}')
        finally:
            shutil.copy(
                f'{multitest_xl}.bak',
                multitest_xl,
            )
            os.remove(f'{multitest_xl}.bak')

    # def test_rxn(self):
    #     """runs the reaction profiling stage"""
    #     shutil.copy(
    #         rxn_xl,
    #         f'{rxn_xl}.bak'
    #     )
    #     try:
    #         rsir = RSIR(
    #             rxn_mz,
    #             bin_numbers=[3, 5, 10],
    #         )
    #         rsir.add_targets_from_xlsx(
    #             rxn_xl,
    #         )
    #         rsir.extract_data()
    #         rsir.write_rsir_to_excel(f'{rxn_xl}')
    #     finally:
    #         shutil.copy(
    #             f'{rxn_xl}.bak',
    #             rxn_xl,
    #         )
    #         os.remove(f'{rxn_xl}.bak')
