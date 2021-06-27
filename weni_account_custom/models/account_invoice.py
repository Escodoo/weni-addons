# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    weni_fiscal_document_url = fields.Char(string='Fiscal Document URL')
    weni_payment_slip_url = fields.Char(string='Payment Slip URL')

    def action_show_fiscal_document(self):
        self.ensure_one()
        url = self.weni_fiscal_document_url
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def action_show_payment_slip(self):
        self.ensure_one()
        url = self.weni_payment_slip_url
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
