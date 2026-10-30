# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import re

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.barcode import get_barcode_check_digit


class ResCompany(models.Model):
    _inherit = 'res.company'

    prefijo_gs1 = fields.Char(
        'GS1 Company Prefix',
        copy=False,
        help='4 to 12 digits assigned by GS1, used as the company part of the SSCC '
             '(Serial Shipping Container Code) generated for each pallet.',
    )

    @api.constrains('prefijo_gs1')
    def _check_prefijo_gs1(self):
        for company in self:
            if company.prefijo_gs1 and not re.fullmatch(r'\d{4,12}', company.prefijo_gs1):
                raise ValidationError(self.env._(
                    'The GS1 Company Prefix of %(company)s must contain 4 to 12 digits.',
                    company=company.name,
                ))

    def _get_sscc_sequence(self):
        """Per-company sequence for the SSCC serial reference, created on first use."""
        self.ensure_one()
        sequence = self.env['ir.sequence'].sudo().search(
            [('code', '=', 'stock.package.sscc'), ('company_id', '=', self.id)],
            order='id', limit=1,
        )
        if not sequence:
            sequence = self.env['ir.sequence'].sudo().create({
                'name': self.env._('SSCC %(company)s', company=self.name),
                'code': 'stock.package.sscc',
                'company_id': self.id,
            })
        return sequence

    def _next_sscc(self, extension_digit='0'):
        """Return a new SSCC: extension digit + GS1 prefix + serial + check digit.

        Returns False when the company has no GS1 Company Prefix configured.
        """
        self.ensure_one()
        if not self.prefijo_gs1:
            return False
        serial = int(self._get_sscc_sequence().next_by_id())
        serial_digits = 16 - len(self.prefijo_gs1)
        if len(str(serial)) > serial_digits:
            raise UserError(self.env._(
                'The SSCC serial reference for %(company)s exceeds %(digits)d digits. '
                'Reset the sequence or use a different GS1 Company Prefix.',
                company=self.name, digits=serial_digits,
            ))
        body = extension_digit + self.prefijo_gs1 + str(serial).zfill(serial_digits)
        return body + str(get_barcode_check_digit(body + '0'))
