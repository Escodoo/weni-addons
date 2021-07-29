# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CrmLeadDecisionMaker(models.Model):

    _name = 'crm.lead.decision.maker'
    _description = 'Crm Lead Decision Maker'

    name = fields.Char()
    lead_id = fields.Many2one(
        'crm.lead',
        string='Lead')
    partner_id = fields.Many2one(
        'res.partner',
        string='Decision Maker')
    decision_maker_type = fields.Selection(
        string='Decision Maker Type',
        selection=[
            ('technical', 'Technical'),
            ('financial', 'Financial'),
            ('user', 'User')
        ],)
