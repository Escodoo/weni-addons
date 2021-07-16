# Copyright 2021 - TODAY, Marcel Savegnago
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    weni_org_id = fields.Char(
        string='Weni Organization ID',
        readonly=True,
        index=True
    )
