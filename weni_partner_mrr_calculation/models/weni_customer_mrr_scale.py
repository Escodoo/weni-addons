# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare


class WeniCustomerMrrScale(models.Model):

    _inherit = "weni.customer.mrr.scale"
    _description = "Customer MRR Scale"

    name = fields.Char("Name")
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.user.company_id,
        string="Company",
        required=False,
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
    )
    min_value = fields.Monetary("Min Value", currency_field="currency_id")
    max_value = fields.Monetary("Max Value", currency_field="currency_id")

    def check_value(self, num, currency):
        self.currency_id = currency
        if (float_compare(num, self.max_value, precision_digits=2) <= 0) and (
            float_compare(num, self.min_value, precision_digits=2) >= 0
        ):
            return True
        return False
