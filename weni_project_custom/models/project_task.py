# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    weni_kanban_state_id = fields.Many2one(
        "project.task.kanban.state",
        string="Weni Kanban State",
    )
    weni_kanban_state_color = fields.Char(
        string="Weni Kanban State Color",
        compute="_compute_weni_kanban_state_color",
    )

    @api.depends("weni_kanban_state_id")
    def _compute_weni_kanban_state_color(self):
        for record in self:
            if record.weni_kanban_state_id:
                record.weni_kanban_state_color = record.weni_kanban_state_id.color
            else:
                record.weni_kanban_state_color = False
