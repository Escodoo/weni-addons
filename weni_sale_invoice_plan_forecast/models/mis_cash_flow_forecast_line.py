# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MisCash_flowForecast_line(models.Model):

    _inherit = "mis.cash_flow.forecast_line"

    sale_invoice_plan_id = fields.Many2one(
        comodel_name="sale.invoice.plan",
        string="Sale Invoice Plan",
        readonly=True,
        ondelete="cascade",
        index=True,
    )

    sale_order_id = fields.Many2one(
        related="sale_invoice_plan_id.sale_id",
        string="Sale Order",
    )
