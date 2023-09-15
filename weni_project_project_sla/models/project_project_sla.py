# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProjectProjectSla(models.Model):

    _name = "project.project.sla"
    _description = "SLA"

    name = fields.Char(string="Name", required=True)
    description = fields.Html("SLA Policy Description", translate=True)
    active = fields.Boolean("Active", default=True)
    duration = fields.Integer(string="Duration (hours)", required=True)
    project_id = fields.Many2one("project.project", "Project", required=True)
    target_stage_id = fields.Many2one(
        comodel_name="project.status", string="Target Stage", required=True
    )
    partner_ids = fields.Many2many(comodel_name="res.partner", string="Partners")
    tag_ids = fields.Many2many(comodel_name="project.tags", string="Tags")
    priority = fields.Selection(
        [
            ("0", "Low"),
            ("1", "Normal"),
        ],
        default="0",
        index=True,
        string="Priority",
    )

    sla_line_ids = fields.One2many(
        "project.project.sla.line", "sla_id", string="SLA Lines", copy=True
    )
    project_ids = fields.One2many(
        "project.project", string="Projects", compute="_compute_project_ids"
    )

    @api.depends("sla_line_ids", "sla_line_ids.project_id")
    def _compute_task_ids(self):
        for sla in self:
            sla.task_ids = sla.sla_line_ids.mapped("project_id")

    _sql_constraints = [
        (
            "duration_positive",
            "CHECK(duration >= 0)",
            "The duration of an SLA must be positive.",
        ),
    ]