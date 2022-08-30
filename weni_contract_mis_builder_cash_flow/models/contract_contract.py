# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    @api.model
    def _get_forecast_update_trigger_fields(self):
        return [
            "partner_id",
            "pricelist_id",
            "fiscal_position_id",
            "currency_id",
            "contract_line_ids",
        ]

    @api.multi
    def write(self, values):
        res = super(ContractContract, self).write(values)
        if any(
            [field in values for field in self._get_forecast_update_trigger_fields()]
        ):
            for rec in self:
                if rec.company_id.enable_contract_mis_cash_flow_forecast:
                    for line in rec.contract_line_ids:
                        line.with_delay()._generate_forecast_lines()
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            for line in rec.contract_line_ids:
                if line.forecast_line_ids:
                    line.forecast_line_ids.unlink()
        return super().unlink()
