# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def _get_forecast_update_trigger_fields(self):
        return [
            "partner_id",
            "state",
            "amount_total",
            "order_line",
            "use_invoice_plan",
            "invoice_plan_ids",
        ]

    @api.multi
    def write(self, values):
        res = super(SaleOrder, self).write(values)
        if any(
            [field in values for field in self._get_forecast_update_trigger_fields()]
        ):
            for rec in self:
                if (
                    rec.use_invoice_plan
                    and rec.company_id.enable_sale_invoice_plan_mis_cash_flow_forecast
                ):
                    for line in rec.invoice_plan_ids:
                        line.with_delay()._generate_forecast_lines()
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            for line in rec.invoice_plan_ids:
                if line.forecast_line_ids:
                    line.forecast_line_ids.unlink()
        return super().unlink()
