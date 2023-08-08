# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailAlias(models.Model):
    _inherit = "mail.alias"

    whitelist_words = fields.Text(
        string="Whitelist Words", help="List of allowed words separated by comma."
    )
