# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons.queue_job.job import job

QUEUE_CHANNEL = "root.SALE_INVOICE_PLAN_MIS_BUILDER_CASH_FLOW"


class SaleInvoicePlan(models.Model):

    _inherit = "sale.invoice.plan"

    forecast_line_ids = fields.One2many(
        comodel_name="mis.cash_flow.forecast_line",
        inverse_name="sale_invoice_plan_id",
        string="Forecast Line",
        required=False,
    )

    @api.multi
    def _prepare_forecast_line(self):
        self.ensure_one()
        return {
            "name": '%s - %s' % (self.sale_id.display_name, self.installment),
            "date": self.plan_date,
            "account_id": self.sale_id.partner_id.property_account_receivable_id.id,
            "partner_id": self.partner_id.id,
            "balance": (self.sale_id.amount_total * self.percent)/100,
            "company_id": self.sale_id.company_id.id,
            "sale_invoice_plan_id": self.id,
        }

    # @api.multi
    # def _get_contract_forecast_end_date(self):
    #     self.ensure_one()
    #     today = fields.Date.context_today(self)
    #     return today + self.get_relative_delta(
    #         self.contract_id.company_id.contract_forecast_rule_type,
    #         self.contract_id.company_id.contract_forecast_interval,
    #     )

    # @api.multi
    # def _get_generate_forecast_periods_criteria(self, period_date_end):
    #     self.ensure_one()
    #     if not self.contract_id.company_id.enable_contract_forecast:
    #         return False
    #     if self.is_canceled or not self.active:
    #         return False
    #     contract_forecast_end_date = self._get_contract_forecast_end_date()
    #     if not self.date_end or self.is_auto_renew:
    #         return period_date_end < contract_forecast_end_date
    #     return (
    #         period_date_end <= self.date_end
    #         and period_date_end <= contract_forecast_end_date
    #     )

    @api.multi
    @job(default_channel=QUEUE_CHANNEL)
    def _generate_forecast_lines(self):
        values = []
        for rec in self:
            rec.forecast_line_ids.unlink()
            if not rec.invoiced and rec.state in ['sale','done']:
                new_vals = rec._prepare_forecast_line()
                values.append(new_vals)

        return self.env["mis.cash_flow.forecast_line"].create(values)

    @api.model
    def create(self, values):
        sale_invoice_plans = super(SaleInvoicePlan, self).create(values)
        for sale_invoice_plan in sale_invoice_plans:
            if sale_invoice_plan.sale_id.company_id.enable_sale_invoice_plan_mis_cash_flow_forecast:
                sale_invoice_plan.with_delay()._generate_forecast_lines()
        return sale_invoice_plans

    @api.model
    def _get_forecast_update_trigger_fields(self):
        return [
            "sale_id",
            "partner_id",
            "state",
            "installment",
            "plan_date",
            "invoice_type",
            "percent",
            "invoice_ids",
            "invoiced",
            "amount_total",
            "order_line"
        ]

    @api.multi
    def write(self, values):
        res = super(SaleInvoicePlan, self).write(values)
        if any(
            [
                field in values
                for field in self._get_forecast_update_trigger_fields()
            ]
        ):
            for rec in self:
                if rec.sale_id.company_id.enable_sale_invoice_plan_mis_cash_flow_forecast:
                    rec.with_delay()._generate_forecast_lines()
        return res

    @api.model
    def cron_generate_forecast_lines(self):
        offset = 0
        while True:
            invoice_plans = self.search(
                ['&',('invoiced', '=', False),('state', 'in', ('sale','done'))], limit=100, offset=offset
            )
            invoice_plans.with_delay()._generate_forecast_lines()
            if len(invoice_plans) < 100:
                break
            offset += 100
