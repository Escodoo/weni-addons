# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniCustomerServiceTypeTask(models.Model):

    _name = "weni.customer.service.type.task"
    _description = "Customer Service Type Task"
    _inherit = ["weni.customer.service.type.task.mixin"]

    customer_service_type_id = fields.Many2one(
        comodel_name="weni.customer.service.type",
        string="Customer Service Type",
        required=True,
    )
