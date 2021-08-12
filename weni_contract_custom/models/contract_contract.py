# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractContract(models.Model):

    _inherit = 'contract.contract'

    @api.multi
    def _prepare_recurring_invoices_values(self, date_ref=False):
        invoices_values = super(ContractContract, self)._prepare_recurring_invoices_values()
        contract_line = self.env["contract.line"]
        consumption_model = self.env["contract.line.consumption"]
        for invoice_values in invoices_values:
            date_invoice = invoice_values.get('date_invoice')

            lines_count = len(invoice_values.get('invoice_line_ids'))

            for line in range(lines_count):

                invoice_line = invoice_values.get('invoice_line_ids')[line]

                contract_line_id = contract_line.search([
                    ('id', '=', dict(invoice_line[2]).get('contract_line_id')),
                ])

                contract_id = contract_line_id.contract_id
                product_id = contract_line_id.product_id
                surplus_product_id = contract_line_id.product_id.surplus_product_id

                invoice_line_vals = contract_line_id._prepare_invoice_line(invoice_values=invoice_values)

                quantity = invoice_line_vals.get('quantity')
                line_price_unit = invoice_line_vals.get('price_unit')

                # TODO: Neste momento não está levando em consideração o periodo.
                consumption_lines = consumption_model.search([('contract_line_id', '=', contract_line_id.id)])
                consumption_quantity = sum(x.consumption_quantity for x in consumption_lines)

                if consumption_quantity > quantity:

                    product_context = dict(self.env.context, partner_id=contract_id.partner_id.id,
                                           date=date_invoice, uom=contract_line_id.uom_id.id)

                    price_unit, rule_id = contract_id.pricelist_id.with_context(product_context).get_product_price_rule(
                        product_id, consumption_quantity or 1.0, contract_id.partner_id)


                    invoice_line_vals['product_id'] = surplus_product_id.id
                    invoice_line_vals['name'] = surplus_product_id.name
                    invoice_line_vals['quantity'] = consumption_quantity - quantity
                    invoice_line_vals['price_unit'] = price_unit or line_price_unit

                    if invoice_line_vals:
                        invoice_values['invoice_line_ids'].append(
                            (0, 0, invoice_line_vals)
                        )

        return invoices_values
