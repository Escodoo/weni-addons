# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLeadChannel(models.Model):  # TODO: remover modelo de dados
    _name = "crm.lead.channel"
    _description = "CRM Lead Channel"

    name = fields.Char()
    lead_ids = fields.Many2many(
        "crm.lead",
        "crm_lead_channel_rel",
        "channel_id",
        "lead_id",
        "Leads",
    )
