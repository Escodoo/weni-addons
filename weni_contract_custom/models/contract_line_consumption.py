# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLineConsumption(models.Model):

    _name = 'contract.line.consumption'
    _description = 'Contract Line Consumption'

    # TODO: Se o consumo for do periodo podemos utilizar o nome
    #  para dar mais consistencia. Em caso negativo, remover
    name = fields.Char()

    contract_line_id = fields.Many2one(
        comodel_name='contract.line',
        index=True)

    consumption_date = fields.Date(
        string='Consumption Date',
        required='true')

    consumption_quantity = fields.Integer(
        string='Consumption Quantity')

    invoice_status = fields.Selection([
        ('invoiced', 'Fully Invoiced'),
        ('to_be_invoice', 'To Invoice'),
    ], string='Invoice Status', readonly=True, default='to_be_invoice'
    )
