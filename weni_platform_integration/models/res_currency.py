# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCurrency(models.Model):

    _inherit = "res.currency"

    weni_id = fields.Char(
        string="Weni ID",
        index=True,
    )
