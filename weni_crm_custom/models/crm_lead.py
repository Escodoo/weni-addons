# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    secondary_user_id = fields.Many2one(
        'res.users',
        string='Pre Salesperson')

    weni_company_size = fields.Integer(
        string='Company Size')

    weni_average_ticket = fields.Monetary(
        'Average Ticket',
        currency_field='company_currency',
        track_visibility='always')

    weni_technological_maturity = fields.Char(
        string="Technological Maturity")

    weni_has_dedicate_team = fields.Boolean(
        string="Has Dedicated Team")

    weni_active_contact = fields.Integer(
        string='Active Contact')

    weni_project_financier = fields.Many2one(
        comodel_name='res.partner',
        string='Project Financier')

    weni_project_budget = fields.Monetary(
        'Budget',
        currency_field='company_currency',
        track_visibility='always')

    weni_project_time_window = fields.Date(
        'Time Window')

    weni_project_gap = fields.Html(
        string='Gap')

    weni_project_gap_primary = fields.Html(
        string='Primary Gap')

    weni_project_gap_secondary = fields.Html(
        string='Secondary Gap')

    weni_project_integration = fields.Html(
        string='Integrations')

    weni_icp_classification = fields.Selection(
        string='ICP Classification',
        selection=[
            ('no_fit', 'No FIT'),
            ('medium_fit', 'Medium FIT'),
            ('high_fit', 'High FIT')
        ],)

    # weni_lead_line_channel_ids = fields.One2many(
    #     comodel_name='crm.lead.line_channel',
    #     inverse_name='lead_id',
    #     string='Lead Channels',
    # )

    weni_channel_ids = fields.Many2many(
        "crm.lead.channel",
        "crm_leed_channel_rel",
        "lead_id",
        "channel_id",
        "Channels",
    )
