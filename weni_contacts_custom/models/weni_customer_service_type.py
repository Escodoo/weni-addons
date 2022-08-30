# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniCustomerServiceType(models.Model):

    _name = "weni.customer.service.type"
    _description = "Customer Service Type"

    name = fields.Char()
