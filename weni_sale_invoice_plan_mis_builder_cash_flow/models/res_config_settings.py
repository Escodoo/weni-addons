# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    enable_sale_invoice_plan_mis_cash_flow_forecast = fields.Boolean(
        string="Enable sale invoice plan on MIS Cashflow forecast",
        default=True,
        readonly=False,
        related="company_id.enable_sale_invoice_plan_mis_cash_flow_forecast",
    )
