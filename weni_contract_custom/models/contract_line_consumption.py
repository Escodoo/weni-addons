# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLineConsumption(models.Model):

    _name = 'contract.line.consumption'
    _description = 'Contract Line Consumption'

    name = fields.Char()

    contract_line_id = fields.Many2one(
        comodel_name='contract.line',
        index=True,
        required='True')

    date_consumption = fields.Date(
        string='Date of Consumption',
        required='true')

    quantity_consumption = fields.Integer(
        string='Quantity Consumption',
        required='True')
