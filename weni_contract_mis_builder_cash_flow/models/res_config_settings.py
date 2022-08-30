# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    enable_contract_mis_cash_flow_forecast = fields.Boolean(
        string="Enable contract on MIS Cashflow forecast",
        default=True,
        readonly=False,
        related="company_id.enable_contract_mis_cash_flow_forecast",
    )
