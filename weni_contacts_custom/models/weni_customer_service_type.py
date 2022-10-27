# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniCustomerServiceType(models.Model):

    _name = "weni.customer.service.type"
    _description = "Customer Service Type"

    name = fields.Char()

    task_ids = fields.One2many(
        comodel_name="weni.customer.service.type.task",
        inverse_name="customer_service_type_id",
        string="Recurrence Tasks",
        required=False,
    )
