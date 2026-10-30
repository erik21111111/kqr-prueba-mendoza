# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.barcode import check_barcode_encoding


class StockPackage(models.Model):
    _inherit = 'stock.package'

    sscc = fields.Char('SSCC', readonly=True, copy=False)

    _sscc_unique = models.Constraint(
        'UNIQUE(sscc)',
        'The SSCC must be unique.',
    )

    @api.constrains('sscc')
    def _check_sscc(self):
        for package in self.filtered('sscc'):
            if not check_barcode_encoding(package.sscc, 'sscc'):
                raise ValidationError(self.env._(
                    'Invalid SSCC %(sscc)s: it must have 18 digits and a valid check digit.',
                    sscc=package.sscc,
                ))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'sscc' not in vals:
                # package.company_id is computed from the contents and is empty at
                # creation time, so the active company owns the SSCC unless one is given.
                company = self.env['res.company'].browse(vals.get('company_id')) or self.env.company
                vals['sscc'] = company._next_sscc()
        return super().create(vals_list)
