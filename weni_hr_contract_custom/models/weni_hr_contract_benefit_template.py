# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WeniHrContractBenefitTemplate(models.Model):

    _name = "weni.hr.contract.benefit.template"
    _description = "Contract Benefit Template"

    name = fields.Char("Name", required=True)
    code = fields.Char("Code", required=True)

    default_value = fields.Float("Default value for this benefit")

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if 'default_value' in vals:
            contract_benefits = self.env['weni.hr.contract.benefit'].search(
                [
                    ('benefit_template_id', '=', self.id),
                    ('contract_state', 'in', ['draft', 'open', 'pending'])
                ]
            )
            for contract_benefit in contract_benefits:
                contract_benefit.amount = vals.get('default_value')
        return res
