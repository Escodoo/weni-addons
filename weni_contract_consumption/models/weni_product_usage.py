# Copyright 2023 - TODAY, Rodrigo Neves Trindade <rodrigo.trindade@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniProductUsage(models.Model):
    _name = "weni.product.usage"
    _description = "Weni Product Usage"

    name = fields.Char(help="The name of the product usage record.")

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        help="The partner associated with this product usage.",
    )

    weni_id = fields.Char(
        string="Weni ID", help="A unique identifier for the Weni project."
    )

    project_uid = fields.Char(
        string="Project UID", help="The unique identifier for the project."
    )

    project_name = fields.Char(string="Project Name", help="The name of the project.")

    date = fields.Date(string="Date", help="The date of the product usage record.")

    active_user_count = fields.Integer(
        string="Active User Count",
        help="The number of active users for this product usage record.",
    )

    channel_uuid = fields.Char(
        string="Channel UUID", help="The unique identifier for the channel."
    )

    channel_name = fields.Char(string="Channel Name", help="The name of the channel.")

    channel_type = fields.Char(string="Channel Type", help="The type of the channel.")

    channel_message_count = fields.Integer(
        string="Channel Message Count", help="The number of messages in the channel."
    )

    flow_uuid = fields.Char(
        string="Flow UUID", help="The unique identifier for the flow."
    )

    flow_name = fields.Char(string="Flow Name", help="The name of the flow.")

    flow_message_count = fields.Integer(
        string="Flow Message Count", help="The number of messages in the flow."
    )

    ia_connect_uuid = fields.Char(
        string="IA Connect UUID", help="The unique identifier for the IA Connect."
    )

    ia_connect_name = fields.Char(
        string="IA Connect Name", help="The name of the IA Connect."
    )

    ia_connect_prediction_count = fields.Integer(
        string="IA Connect Prediction Count",
        help="The number of predictions made by the IA Connect.",
    )

    human_service_department = fields.Char(
        string="Human Service Department",
        help="The department associated with the human service.",
    )

    human_service_qrd_service_count = fields.Integer(
        string="Human Service QRD Service Count",
        help="The number of QRD services provided by the human service.",
    )

    human_agent_count = fields.Integer(
        string="Human Agent Count",
        help="The number of human agents associated with this product usage record.",
    )

    login_count = fields.Integer(
        string="Login Count",
        help="The number of logins associated with this product usage record.",
    )
