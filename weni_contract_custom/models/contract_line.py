# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLine(models.Model):

    _inherit = 'contract.line'

    # @api.multi
    # def _prepare_invoice_line(
    #     self, invoice_id=False, invoice_values=False
    # ):
    #     values = super()._prepare_invoice_line(
    #         invoice_id, invoice_values)
    #     if self.automatic_price:
    #         date_invoice = invoice_values['date_invoice']
    #         product_context = dict(self.env.context, partner_id=self.contract_id.partner_id.id,
    #                                date=date_invoice, uom=self.uom_id.id)
    #         price_unit, rule_id = self.contract_id.pricelist_id.with_context(product_context).get_product_price_rule(
    #             self.product_id, values['quantity'] or 1.0, self.contract_id.partner_id)
    #         values.update({'price_unit': price_unit})
    #     return values
