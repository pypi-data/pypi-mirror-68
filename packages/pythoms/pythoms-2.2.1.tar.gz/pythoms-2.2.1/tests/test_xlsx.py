import os
import unittest

from pythoms.xlsx import XLSX


class TestXLSX(unittest.TestCase):
    def test_xlsx(self):
        xlfile = XLSX(
            os.path.join(os.path.dirname(__file__), 'xlsx_validation'),
            verbose=False
        )
        spec, xunit, yunit = xlfile.pullspectrum('example MS spectrum')
        multispec = xlfile.pullmultispectrum('example multi-spectrum')
        rsimparams = xlfile.pullrsimparams()
        xlout = XLSX(
            'xlsxtestout.xlsx',
            create=True,
            verbose=False
        )
        xlout.writespectrum(spec[0], spec[1], 'test single spectrum out', xunit, yunit)
        for key, val in sorted(multispec.items()):
            xlout.writemultispectrum(
                multispec[key]['x'],
                multispec[key]['y'],
                multispec[key]['xunit'],
                multispec[key]['yunit'],
                'Function Chromatograms',
                key
            )
        xlout.save()
        os.remove(
            'xlsxtestout.xlsx'
        )
