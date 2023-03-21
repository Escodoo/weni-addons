# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.fields import date


class ResPartnerServiceTypeTask(models.Model):
    _name = "res.partner.service.type.task"
    _description = "Partner Service Type Task"
    _inherit = ["weni.customer.service.type.task.mixin"]

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )

    date_next_recurrence = fields.Date(
        string="Date of Next Recurrence",
        compute="_compute_date_next_recurrence",
        store=True,
        readonly=False,
    )

    date_last_recurrence = fields.Date(
        string="Date of Next Recurrence", readonly="True"
    )

    template_task_id = fields.Many2one(
        comodel_name="weni.customer.service.type.task",
        string="Template Task",
        required=False,
    )

    @api.depends(
        "day_of_month", "recurrence_count", "recurrence_unit", "date_last_recurrence"
    )
    def _compute_date_next_recurrence(self):
        for task in self:
            if task.recurrence_unit == "days":
                task.date_next_recurrence = (
                    task.date_last_recurrence
                    or date.today() + relativedelta(days=task.recurrence_count)
                )
            elif task.recurrence_unit == "weeks":
                task.date_next_recurrence = (
                    task.date_last_recurrence
                    or date.today() + relativedelta(days=7 * task.recurrence_count)
                )
            elif task.recurrence_unit == "months":
                task.date_next_recurrence = (
                    task.date_last_recurrence
                    or date.today() + relativedelta(months=task.recurrence_count)
                )
                if task.day_of_month:
                    date_next_recurrence = task.date_next_recurrence.replace(
                        day=task.day_of_month
                    )
                    if date_next_recurrence < date.today():
                        task.date_next_recurrence = (
                            task.date_next_recurrence + relativedelta(months=+1)
                        ).replace(day=task.day_of_month)
                    else:
                        task.date_next_recurrence = date_next_recurrence
