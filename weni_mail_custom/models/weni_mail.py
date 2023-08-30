# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class WeniMailBlacklist(models.Model):
    _name="weni.mail.blacklist"
    _description = "Weni Mail Blacklist"

    alias_id = fields.Many2one("mail.alias", required=True, ondelete="cascade")
    weni_blacklist_mail = fields.Char(required=True)