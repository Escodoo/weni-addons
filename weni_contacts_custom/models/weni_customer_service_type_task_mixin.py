# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniCustomerServiceTypeTaskMixin(models.AbstractModel):
    _name = "weni.customer.service.type.task.mixin"
    _description = "Customer Service Type Task Mixin"

    name = fields.Char(string="Summary")

    activity_type_id = fields.Many2one(
        "mail.activity.type", "Activity", ondelete="restrict"
    )

    note = fields.Html("Note", sanitize_style=True)

    user_id = fields.Many2one(
        "res.users",
        "Assigned to",
        default=lambda self: self.env.user,
        index=True,
        required=True,
    )

    recurrence_count = fields.Integer(
        "Recurrence Count",
        default=1,
        help="Number of days/week/month executing the action. It allows to "
        "plan the action deadline.",
        required=True,
    )

    recurrence_unit = fields.Selection(
        [("days", "days"), ("weeks", "weeks"), ("months", "months")],
        string="Recurrence units",
        help="Unit of delay",
        required=True,
        default="days",
    )

    day_of_month = fields.Integer("Day of Month", default=0)
