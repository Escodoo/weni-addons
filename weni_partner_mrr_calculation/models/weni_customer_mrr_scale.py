# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniCustomerMrrScale(models.Model):
    _inherit = "weni.customer.mrr.scale"
    _description = "Customer MRR Scale"

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.user.company_id,
        string="Company",
        required=True,
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
    )
    min_value = fields.Monetary("Min Value", currency_field="currency_id")
    max_value = fields.Monetary("Max Value", currency_field="currency_id")
