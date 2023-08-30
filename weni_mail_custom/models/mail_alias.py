# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailAlias(models.Model):
    _inherit = "mail.alias"

    weni_mail_blacklist_ids = fields.One2many(
        "weni.mail.blacklist", "alias_id", string="Weni Mail lines", copy=True
    )