# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTaskKanbanState(models.Model):
    _name = "project.task.kanban.state"
    _description = "Project Task Kanban State"

    name = fields.Char(string="Name", required=True)
    color = fields.Char(string="Color", required=True, help="Choose a color")

    @api.model
    def search_records_by_name(self, selection_item):
        domain = [("name", "=", selection_item)]
        records = self.search(domain)
        result = []
        for record in records:
            result.append(
                {
                    "name": record.name,
                    "color": record.color,
                }
            )
        return result
