# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime
from odoo import api, fields, models, _


class ContractContract(models.Model):

    _inherit = 'contract.contract'

    contract_consumption_ids = fields.One2many(
        'contract.line.consumption',
        'contract_id',
        'Contract Consumption'
    )

    contract_consumption_count = fields.Integer(
        compute="_compute_contract_consumption",
        string='# Contract Consumption Count')

    @api.depends('contract_consumption_ids')
    def _compute_contract_consumption(self):
        for rec in self:
            rec.contract_consumption_count = len(
                rec.contract_consumption_ids)

    @api.model
    def _finalize_invoice_creation(self, invoices):
        super()._finalize_invoice_creation(invoices)

        consumption_model = self.env["contract.line.consumption"]

        for invoice in invoices:
            period_date_start = invoice.date_invoice.replace(day=1)

            for line in invoice.invoice_line_ids:
                contract_line_id = line.contract_line_id
                contract_id = contract_line_id.contract_id

                if contract_id.contract_type == 'sale':

                    consumption_lines = consumption_model.search(
                        [
                            ('contract_line_id', '=', contract_line_id.id),
                            ('consumption_date', '<', period_date_start),
                            ('invoice_status', '=', 'to_be_invoice')
                        ]
                    )

                    consumption_quantity = sum(
                        x.consumption_quantity for x in consumption_lines
                    )

                    if consumption_quantity > line.quantity:

                        product_context = dict(
                            self.env.context,
                            partner_id=contract_id.partner_id.id,
                            date=invoice.date_invoice,
                            uom=contract_line_id.uom_id.id
                        )

                        price_unit, rule_id = contract_id.pricelist_id.with_context(
                            product_context).get_product_price_rule(
                            line.product_id,
                            consumption_quantity or 1.0,
                            contract_id.partner_id
                        )

                        line.quantity = consumption_quantity

                        if price_unit != line.product_id.list_price:
                            line.price_unit = price_unit

                        line._onchange_fiscal_operation_id()

                        for consumption in consumption_lines:
                            consumption.invoice_status = 'invoiced'

            invoice._onchange_invoice_line_ids()

    @api.multi
    def action_view_contract_consumption(self):
        action = self.env.ref(
            "weni_contract_consumption.contract_line_consumption_act_window").read()[0]
        if self.contract_consumption_count > 1:
            action["domain"] = [("id", "in", self.contract_consumption_ids.ids)]
        else:
            action["views"] = [(
                self.env.ref(
                    "weni_contract_consumption.contract_line_consumption_form_view").id,
                "form"
            )]
            action["res_id"] = \
                self.contract_consumption_ids and self.contract_consumption_ids.ids[0] or False
        return action
