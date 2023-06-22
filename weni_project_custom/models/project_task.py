# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    kanban_state = fields.Selection(
        selection="_get_kanban_state_selection", string="Kanban State"
    )
    kanban_state_label = fields.Char(
        compute="_compute_kanban_state_label",
        string="Kanban State Label",
        track_visibility="onchange",
    )

    def _get_kanban_state_selection(self):
        default_states = [
            ("normal", "Grey"),
            ("done", "Green"),
            ("blocked", "Red"),
        ]
        weni_states = (
            self.env["project.task.kanban.state"]
            .search([])
            .mapped(lambda state: (state.name, state.color))
        )
        return default_states + weni_states

    @api.depends("stage_id", "kanban_state")
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == "normal":
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == "blocked":
                task.kanban_state_label = task.legend_blocked
            else:
                weni_states = self.env["project.task.kanban.state"].search(
                    [("name", "=", task.kanban_state)]
                )
                if weni_states:
                    task.kanban_state_label = weni_states.name
                else:
                    task.kanban_state_label = task.legend_done
