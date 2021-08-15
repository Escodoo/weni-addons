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

    # @api.multi
    # def _prepare_recurring_invoices_values(self, date_ref=False):
    #     invoices_values = super(
    #         ContractContract, self)._prepare_recurring_invoices_values()
    #
    #     contract_line_model = self.env["contract.line"]
    #     consumption_model = self.env["contract.line.consumption"]
    #
    #     for invoice_values in invoices_values:
    #         date_invoice = invoice_values.get('date_invoice')
    #         lines_count = len(invoice_values.get('invoice_line_ids'))
    #
    #         for line in range(lines_count):
    #
    #             invoice_line = invoice_values.get('invoice_line_ids')[line]
    #
    #             contract_line_id = contract_line_model.search([
    #                 ('id', '=', dict(invoice_line[2]).get('contract_line_id')),
    #             ])
    #
    #             contract_id = contract_line_id.contract_id
    #             product_id = contract_line_id.product_id
    #             surplus_product_id = product_id.surplus_product_id or product_id
    #
    #             invoice_line_vals = contract_line_id._prepare_invoice_line(
    #                 invoice_values=invoice_values
    #             )
    #
    #             quantity = invoice_line_vals.get('quantity')
    #             line_price_unit = invoice_line_vals.get('price_unit')
    #
    #             period_date_start = date_invoice.replace(day=1)
    #             # period_date_end = period_date_start - datetime.timedelta(days=45)
    #
    #             consumption_lines = consumption_model.search(
    #                 [
    #                     ('contract_line_id', '=', contract_line_id.id),
    #                     ('consumption_date', '<', period_date_start),
    #                     ('invoice_status', '=', 'to_be_invoice')
    #                 ]
    #             )
    #
    #             consumption_quantity = sum(
    #                 x.consumption_quantity for x in consumption_lines
    #             )
    #
    #             if consumption_quantity > quantity:
    #
    #                 product_context = dict(
    #                     self.env.context,
    #                     partner_id=contract_id.partner_id.id,
    #                     date=date_invoice,
    #                     uom=contract_line_id.uom_id.id
    #                 )
    #
    #                 price_unit, rule_id = contract_id.pricelist_id.with_context(
    #                     product_context).get_product_price_rule(
    #                     product_id,
    #                     consumption_quantity or 1.0,
    #                     contract_id.partner_id
    #                 )
    #
    #                 invoice_line_vals['product_id'] = surplus_product_id.id
    #                 invoice_line_vals['name'] = surplus_product_id.name
    #                 invoice_line_vals['quantity'] = consumption_quantity - quantity
    #                 invoice_line_vals['price_unit'] = price_unit or line_price_unit
    #
    #                 if invoice_line_vals:
    #                     invoice_values['invoice_line_ids'].append(
    #                         (0, 0, invoice_line_vals)
    #                     )
    #
    #                 for consumption in consumption_lines:
    #                     consumption.invoice_status = 'invoiced'
    #
    #     return invoices_values

    @api.model
    def _finalize_invoice_creation(self, invoices):
        super()._finalize_invoice_creation(invoices)

        consumption_model = self.env["contract.line.consumption"]
        invoice_line_model = self.env["account.invoice.line"]

        for invoice in invoices:
            period_date_start = invoice.date_invoice.replace(day=1)

            for line in invoice.invoice_line_ids:
                contract_line_id = line.contract_line_id
                contract_id = contract_line_id.contract_id

                if contract_id.contract_type == 'sale':
                    surplus_product_id = (
                            line.product_id.surplus_product_id or
                            line.product_id)

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

                        consumption = consumption_quantity - line.quantity

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

                        account = (
                                surplus_product_id.property_account_income_id or
                                surplus_product_id.categ_id.property_account_income_categ_id
                        )

                        fpos = invoice.fiscal_position_id or invoice.partner_id.property_account_position_id
                        if fpos and account:
                            account = fpos.map_account(account)

                        new_invoice_line = invoice_line_model.create({

                            'invoice_id': invoice.id,
                            'name': surplus_product_id.name,
                            'product_id': surplus_product_id.id,
                            'price_unit': price_unit,
                            'quantity': consumption,
                            'account_id': account.id,
                            'fiscal_operation_id': invoice.fiscal_operation_id.id,
                        })

                        new_invoice_line._onchange_product_id_fiscal()
                        new_invoice_line.price_unit = price_unit

                        new_invoice_line._onchange_fiscal_operation_id()
                        new_invoice_line._onchange_fiscal_tax_ids()

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
