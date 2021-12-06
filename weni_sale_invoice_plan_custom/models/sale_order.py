# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from datetime import date, datetime

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.model
    def _cron_sale_invoice_plan(self):

        sale_order_ids = self.env['sale.order'].search(
            [
                ('use_invoice_plan', '=', True),
                ('invoice_status', '=', 'to invoice')
            ]
        )
        sale_orders_invoiced = []
        for sale in sale_order_ids:

            invoice_plans = sale.invoice_plan_ids.filtered(
                lambda l: not l.invoiced and l.plan_date <= fields.Date.today())
            for plan in invoice_plans:
                task_open = plan.project_task_ids.filtered(
                    lambda l: not l.stage_id.closed)

            if invoice_plans and not task_open:
                ctx = {'active_id': sale.id,
                       'active_ids': [sale.id],
                       'all_remain_invoices': False}

                make_wizard = sale.env['sale.make.planned.invoice'].create({})
                make_wizard.with_context(ctx).create_invoices_by_plan()
                sale_orders_invoiced += sale

        return sale_orders_invoiced or False

    @api.model
    def _get_sale_orders_domain(self):
        domain = [
            ('use_invoice_plan', '=', True),
            ('invoice_status', '=', 'to invoice'),
        ]
        return domain

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        inv_ids = super().action_invoice_create(grouped=grouped, final=final)
        invoice_plan_id = self._context.get('invoice_plan_id')
        if invoice_plan_id:
            plan = self.env['sale.invoice.plan'].browse(invoice_plan_id)
            invoices = self.env['account.invoice'].browse(inv_ids)
            invoices.ensure_one()  # Expect 1 invoice for 1 invoice plan
            invoices[0].comment += 'This invoice refers to: ' + plan.description
        return inv_ids
