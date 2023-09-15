# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProjectProjectSlaLine(models.Model):

    _name = "project.project.sla.line"
    _description = "SLA Line"

    _order = "deadline"

    project_id = fields.Many2one(comodel_name="project.project", string="Project")
    sla_id = fields.Many2one(comodel_name="project.project.sla", string="SLA")
    status = fields.Selection(
        selection=[("not_met", "Not Met"), ("met", "Met")], string="Status"
    )
    deadline = fields.Datetime(
        string="Deadline",
    )
    reached_date = fields.Datetime(string="Reached Date")
    sla_target_stage_id = fields.Many2one(
        comodel_name="project.status",
        string="Target Stage",
        related="sla_id.target_stage_id",
    )
