# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WeniHrContractBenefit(models.Model):

    _name = "weni.hr.contract.benefit"
    _description = "Contract Benefit"

    contract_id = fields.Many2one("hr.contract")

    contract_state = fields.Selection(related="contract_id.state")

    benefit_template_id = fields.Many2one(
        "weni.hr.contract.benefit.template", string="Benefit Template"
    )

    benefit_template_code = fields.Char(
        string="Code", related="benefit_template_id.code", readonly=True
    )

    amount = fields.Float(string="Amount")

    @api.onchange("benefit_template_id")
    def _onchange_benefit_template_id(self):
        for record in self:
            record.amount = record.benefit_template_id.default_value
