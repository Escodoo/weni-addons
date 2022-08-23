# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniCustomerStatus(models.Model):

    _name = "weni.customer.status"
    _description = "Customer Status"

    name = fields.Char()
