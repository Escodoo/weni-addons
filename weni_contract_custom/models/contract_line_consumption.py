# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLineConsumption(models.Model):

    _name = 'contract.line.consumption'
    _description = 'Contract Line Consumption'
    _rec_name = 'contract_line_id'

    # name = fields.Char(string='Name', required=True, index=True, copy=False,
    #                    default=lambda self: _('New'))

    contract_id = fields.Many2one(
        comodel_name='contract.contract',
        index=True,
        required='True',
    )

    contract_line_id = fields.Many2one(
        comodel_name='contract.line',
        index=True,
        required='True',
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

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         if vals.get('contract_id'):
    #             contract_id = vals.get('contract_id')
    #             contract = self.env['contract.contract'].browse(contract_id)
    #
    #         if vals.get('contract_line_id'):
    #             contract_line_id = vals.get('contract_line_id')
    #             contract_line = self.env['contract.line'].browse(contract_line_id)
    #
    #         vals['name'] = contract.name + ' - ' + contract_line.name \
    #             or _('New')
    #
    #     return super(ContractLineConsumption, self).create(vals)
    #
    #
    # def write(self, vals):
    #     if 'contract_id' in vals or 'contract_line_id' in vals:
    #         if vals.get('contract_id'):
    #             contract_id = vals.get('contract_id')
    #             contract = self.env['contract.contract'].browse(contract_id)
    #
    #         if vals.get('contract_line_id'):
    #             contract_line_id = vals.get('contract_line_id')
    #             contract_line = self.env['contract.line'].browse(contract_line_id)
    #
    #         vals['name'] = contract.name + ' - ' + contract_line.name \
    #             or _('New')
    #
    #     return super().write(vals)