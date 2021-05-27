# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CrmLeadUser(models.Model):

    _name = 'crm.lead.user'
    _description = 'Crm Lead User'  # TODO

    name = fields.Char()
    lead_id = fields.Many2one(
        'crm.lead',
        string='Lead')
    user_id = fields.Many2one(
        'res.partner',
        string='User')
    function = fields.Char(
        related='user_id.function',
        string='Job Position')
    email = fields.Char(
        related='user_id.email',
        readonly=True)
    phone = fields.Char(related='user_id.phone')
    mobile = fields.Char(related='user_id.mobile')
