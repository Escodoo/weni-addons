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
    weni_average_selling_price = fields.Monetary(
        'Average Selling Price',
        currency_field='company_currency',
        track_visibility='always')
    weni_technological_maturity = fields.Selection(
        string='Technological Maturity',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],)
    weni_has_dedicate_team = fields.Boolean(
        string="Has Dedicated Team")
    weni_active_contacts = fields.Integer(
        string='Active Contacts')
    weni_project_budget = fields.Monetary(
        'Budget',
        currency_field='company_currency',
        track_visibility='always')
    weni_project_release_date = fields.Date(
        'Release Date')
    weni_project_pain_primary = fields.Html(
        string='Primary Pains')
    weni_project_pain_secondary = fields.Html(
        string='Secondary Pains')
    weni_project_integration = fields.Html(
        string='Integrations')
    weni_icp_classification = fields.Selection(
        string='ICP Classification',
        selection=[
            ('no_fit', 'No Fit'),
            ('medium_fit', 'Medium Fit'),
            ('high_fit', 'High Fit')
        ],)
    weni_channel_ids = fields.Many2many(
        "crm.lead.channel",
        "crm_leed_channel_rel",
        "lead_id",
        "channel_id",
        "Channels",
    )
    weni_decision_maker_ids = fields.One2many(
        comodel_name='crm.lead.decision.maker',
        inverse_name='lead_id',
        string='Lead Lines',
    )
    weni_user_ids = fields.One2many(
        comodel_name='crm.lead.user',
        inverse_name='lead_id',
        string='Users',
    )
    weni_sale_type = fields.Selection(
        string='Sale Type',
        selection=[
            ('project', 'Project'),
            ('platform', 'Platform'),
        ],)
