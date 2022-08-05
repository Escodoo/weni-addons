# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class WeniCustomerStatus(models.Model):

    _name = "weni.customer.status"
    _description = "Customer Status"

    name = fields.Char()
    weni_generate_nps = fields.Boolean(string="Generate NPS", default=False)