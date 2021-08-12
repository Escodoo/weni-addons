# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLineForecastPeriod(models.Model):

    _inherit = 'contract.line.forecast.period'

    # @api.multi
    # def _compute_price_subtotal(self):
    #     # TODO: Herdar e alterar o valor. Ou migrar para OCA
    #     for line in self:
    #         subtotal = line.quantity * line.price_unit
    #         discount = line.discount / 100
    #         subtotal *= 1 - discount
    #         if line.contract_id.pricelist_id:
    #             cur = line.contract_id.pricelist_id.currency_id
    #             if line.contract_line_id.automatic_price:
    #                 product_context = dict(line.env.context, partner_id=line.contract_id.partner_id.id,
    #                                        date=line.date_invoice, uom=line.product_id.uom_id.id)
    #                 price, rule_id = line.contract_id.pricelist_id.with_context(product_context).get_product_price_rule(
    #                     line.product_id, line.quantity or 1.0, line.contract_id.partner_id)
    #                 subtotal = line.quantity * price
    #             line.price_subtotal = cur.round(subtotal)
    #         else:
    #             line.price_subtotal = subtotal