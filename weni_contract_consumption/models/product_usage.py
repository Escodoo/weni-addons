# Copyright 2023 Escodoo - Rodrigo Neves Trindade
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductUsage(models.Model):

    _name = "product.usage"
    _description = "Product Usage"

    name = fields.Char()  

    partner_id = fields.Many2one(
        'res.partner', string='Partner'
    )

    weni_id = fields.Char(
        string="Weni ID",
    )

    project_uid = fields.Char(
        string='Project UID'
    )

    project_name = fields.Char(
        string='Project Name'
    )

    date = fields.Date(
        string='Date'
    )

    active_user = fields.Integer(
        string='Active User'
    )

    channels_uuid = fields.Char(
        string='Channels'
    )

    channels_name = fields.Char(
        string='Name Channels'
    )

    channel_type = fields.Char(
        string='Type Channels'
    )

    channels_qtdmsg= fields.Integer(
        string='Quantity of Messages'
    )

    flows_uuid = fields.Char(
        string='Flows'
    )

    flows_name = fields.Char(
        string='Name Flow'
    )

    flows_qtdmsg = fields.Integer(
        string='Flow Rate'
    )

    ia_connect_uuid = fields.Char(
        string='IA Connect'
    )

    ia_connect_name = fields.Char(
        string='IA Name'
    )

    ia_connect_qtdprediction = fields.Integer(
        string='Quantity of Prediction'
    )

    human_service_department = fields.Char(
        string='Human Service Department'
    )

    human_service_qrd_service = fields.Integer(
        string='Human Service Qrd Service'
    )

    human_agents_qty = fields.Integer(
        string='Quantity of Human Agents'
    )

    logins_qty = fields.Integer(
        string='Quantity of Logins'
    )

