# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # Main
    secondary_user_id = fields.Many2one("res.users", string="Pre Salesperson")
    planned_revenue = fields.Monetary(string="Monthly Recurring Revenue")
    weni_amount_nrr = fields.Monetary(
        "Amount NRR",
        currency_field="company_currency",
        track_visibility="always",
        help="Amount Non-Recurring Revenue",
    )
    weni_project_release_date = fields.Date("Release Date")
    weni_sale_type = fields.Selection(
        string="Sale Type",
        selection=[
            ("platform", "Platform"),
            ("project", "Project"),
            ("enterprise", "Enterprise Project"),
        ],
    )
    weni_sale_sector = fields.Char(string="Sector")
    weni_sector_demand = fields.Char(string="Demand Sector")
    weni_linkedin_profile = fields.Char(string="Linkedin Profile")
    weni_lost_date = fields.Date("Lost Date", track_visibility="always")
    weni_is_freezed = fields.Boolean(string="Is freezed")

    # ICP Details
    weni_company_size = fields.Selection(
        string="Company Size",
        selection=[
            ("mb", "Microbusiness"),
            ("smb", "Small and Medium-sized Business"),
            ("msb", "Medium-sized Business"),
            ("lsb", "Large-sized Business"),
        ],
    )

    weni_active_contacts = fields.Integer(string="Active Contacts")
    weni_has_dedicate_team = fields.Boolean(string="Has Dedicated Team")
    weni_customer_rating = fields.Float(string="Company Rating")
    weni_total_human_agents = fields.Integer(string="Total Human Agents")
    weni_use_chatbot_solution = fields.Boolean(string="Use Chatbot Solution")
    weni_systems_used = fields.Html(string="Systems Used")
    weni_icp_classification = fields.Selection(
        string="ICP Classification",
        selection=[
            ("no_fit", "No Fit"),
            ("medium_fit", "Medium Fit"),
            ("high_fit", "High Fit"),
        ],
    )

    # Diagnostic
    weni_current_situation = fields.Html(string="Current Situation")
    weni_project_pain_primary = fields.Html(string="Primary Problems")
    weni_project_pain_secondary = fields.Html(string="Secondary Problems")
    weni_implication = fields.Html(string="Implication")
    weni_need = fields.Html(string="Need")
    weni_project_integration = fields.Html(string="Integrations")
    weni_channels_used = fields.Html(string="Channels Used")

    # TODO: Não vão utilizar
    weni_channel_ids = fields.Many2many(
        "crm.lead.channel",
        "crm_leed_channel_rel",
        "lead_id",
        "channel_id",
        "Channels",
    )

    # Decision Makers
    weni_decision_maker_ids = fields.One2many(
        comodel_name="crm.lead.decision.maker",
        inverse_name="lead_id",
        string="Decision Markers",
    )
    weni_user_ids = fields.One2many(
        comodel_name="crm.lead.user",
        inverse_name="lead_id",
        string="Users",
    )

    weni_automation = fields.Boolean(string="Weni Automation")
    weni_qualified = fields.Boolean(string="Qualified ?")
    weni_no_show = fields.Boolean(string="No Show")

    # RD Fields
    rd_created_date = fields.Date(string="Created Date")
    rd_first_conversion_date = fields.Date(string="First Conversion Date")
    rd_conversion_origin = fields.Char(string="Conversion Origin")
    rd_odoo_lead_link = fields.Char(string="Lead RD Link")
    rd_actions_history = fields.Html(string="Actions History")

    weni_monthly_attendance_number = fields.Char(string="Monthly Attendance Number")
    weni_customer_profile = fields.Selection(
        string="Customer Profile",
        selection=[
            ("enterprise", "Enterprise"),
            ("startups_tech", "Startups / Tech"),
            ("middle_market", "Middle Market"),
            ("civic_engagement", "Civic Engagement"),
            ("other", "Other"),
        ],
    )
    weni_last_source_attribution = fields.Char(string="Last Source Attribution")
    weni_first_source_attribution = fields.Char(string="First Source Attribution")
    weni_multi_source_attribution = fields.Char(string="Multi Source Attribution")
    weni_fbclid = fields.Char(string="Fbclid")
    weni_gclid = fields.Char(string="Gclid")
    weni_utm_source = fields.Char(string="UTM Source")
    weni_utm_medium = fields.Char(string="UTM Medium")
    weni_utm_campaign = fields.Char(string="UTM Campaign")
    weni_utm_content = fields.Char(string="UTM Content")
    weni_utm_term = fields.Char(string="UTM Term")
    weni_client_user_agent = fields.Char(string="Client User Agent")
    weni_client_ip_address = fields.Char(string="Client Ip Address")
    weni_analytics_client_id = fields.Char(string="Analytics Client ID")
    
    @api.multi
    def action_set_lost(self):
        super().action_set_lost()
        return self.write({"weni_lost_date": date.today()})

    def toggle_active(self):
        res = super().toggle_active()
        for lead in self.filtered(lambda lead: lead.active):
            lead.lost_reason = False
            lead.weni_lost_date = False
        return res
