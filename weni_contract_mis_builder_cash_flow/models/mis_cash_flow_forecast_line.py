# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MisCashFlowForecastLine(models.Model):

    _inherit = "mis.cash_flow.forecast_line"

    contract_line_id = fields.Many2one(
        comodel_name="contract.line",
        string="Contract Line",
        readonly=True,
        ondelete="cascade",
        index=True,
    )

    contract_id = fields.Many2one(
        related="contract_line_id.contract_id",
        string="Contract",
    )
