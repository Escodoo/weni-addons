# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniPartnerNpsChannel(models.Model):
    _name = "weni.partner.nps.channel"
    _description = "NPS Channel"

    name = fields.Char()
