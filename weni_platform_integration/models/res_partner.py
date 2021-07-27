# Copyright 2021 - TODAY, Marcerl Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    weni_id = fields.Char(
        string='Weni ID',
        index=True,
    )
