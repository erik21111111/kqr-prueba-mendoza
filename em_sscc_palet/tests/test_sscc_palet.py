# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from psycopg2 import IntegrityError

from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger
from odoo.tools.barcode import check_barcode_encoding


@tagged('post_install', '-at_install')
class TestSsccPalet(TransactionCase):
    """SSCC generation on stock.package, with the GS1 prefixes of the test case."""

    def setUp(self):
        super().setUp()
        # Fresh companies per test so that their SSCC sequences start at 1.
        self.company_a = self.env['res.company'].create({
            'name': 'Compañía A', 'prefijo_gs1': '8412345',
        })
        self.company_b = self.env['res.company'].create({
            'name': 'Compañía B', 'prefijo_gs1': '841234567',
        })

    def _create_pallets(self, company, count=1):
        return self.env['stock.package'].with_company(company).create(
            [{} for _ in range(count)])

    def test_gs1_public_example(self):
        """Public GS1 example: 1 + 0614141 + 123456789 + check digit 7."""
        company = self.env['res.company'].create({
            'name': 'GS1 Example', 'prefijo_gs1': '0614141',
        })
        company._get_sscc_sequence().number_next_actual = 123456789
        self.assertEqual(company._next_sscc(extension_digit='1'), '106141411234567897')

    def test_company_a_sscc(self):
        pallets = self._create_pallets(self.company_a, count=2)
        self.assertEqual(pallets[0].sscc, '084123450000000010')
        self.assertEqual(pallets[1].sscc, '084123450000000027')
        for pallet in pallets:
            self.assertEqual(len(pallet.sscc), 18)
            self.assertTrue(pallet.sscc.startswith('08412345'))
            self.assertTrue(check_barcode_encoding(pallet.sscc, 'sscc'))

    def test_company_b_sscc(self):
        pallets = self._create_pallets(self.company_b, count=2)
        self.assertEqual(pallets[0].sscc, '084123456700000015')
        self.assertEqual(pallets[1].sscc, '084123456700000022')
        for pallet in pallets:
            self.assertTrue(pallet.sscc.startswith('0841234567'))
            self.assertTrue(check_barcode_encoding(pallet.sscc, 'sscc'))

    def test_sscc_unique(self):
        """The prefixes of A and B overlap: serial 670000001 of A collides
        with serial 1 of B. The unique constraint must reject it."""
        pallet_b = self._create_pallets(self.company_b)
        self.assertEqual(pallet_b.sscc, '084123456700000015')
        self.company_a._get_sscc_sequence().number_next_actual = 670000001
        with self.assertRaises(IntegrityError), self.cr.savepoint(), \
                mute_logger('odoo.sql_db'):
            self._create_pallets(self.company_a)

    def test_sscc_empty_without_prefix(self):
        """No GS1 prefix configured: the pallet is created without SSCC."""
        pallet = self.env['stock.package'].create({})
        self.assertFalse(self.env.company.prefijo_gs1)
        self.assertFalse(pallet.sscc)
