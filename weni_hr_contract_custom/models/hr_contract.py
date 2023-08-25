# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrContract(models.Model):

    _inherit = "hr.contract"

    weni_benefit_ids = fields.One2many(
        comodel_name='weni.hr.contract.benefit',
        inverse_name='contract_id',
        string='Contract Benefits',
    )

    weni_benefit_total_amount = fields.Monetary(string='Total Benefit Amount', store=True, readonly=True, compute='_compute_amount_all')

    @api.depends('weni_benefit_ids.amount')
    def _compute_amount_all(self):
        for contract in self:
            amount = 0
            for benefit in contract.weni_benefit_ids:
                amount += benefit.amount
            contract.update({
                'weni_benefit_total_amount': amount,
            })
