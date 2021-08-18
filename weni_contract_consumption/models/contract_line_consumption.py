# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLineConsumption(models.Model):

    _name = 'contract.line.consumption'
    _description = 'Contract Line Consumption'
    _rec_name = 'contract_line_id'

    contract_id = fields.Many2one(
        comodel_name='contract.contract',
        index=True,
        required='True',
    )

    partner_id = fields.Many2one(
        related='contract_id.partner_id',
        string='Partner',
        store='True',
    )

    contract_line_id = fields.Many2one(
        comodel_name='contract.line',
        index=True,
        required='True',
    )

    product_id = fields.Many2one(
        related='contract_line_id.product_id',
        string='Product',
        store = 'True',
    )

    consumption_date = fields.Date(
        string='Consumption Date',
        index=True,
        required='True'
    )

    consumption_quantity = fields.Integer(
        string='Consumption Quantity')

    invoice_status = fields.Selection([
        ('invoiced', 'Fully Invoiced'),
        ('to_be_invoice', 'To Invoice'),
    ], string='Invoice Status', readonly=True, default='to_be_invoice'
    )

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        for rec in self:
            rec.contract_line_id = False
