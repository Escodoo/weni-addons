# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTaskKanbanState(models.Model):
    _name = "project.task.kanban.state"
    _description = "Project Task Kanban State"

    name = fields.Char(string="Name", required=True)
    color = fields.Char(string="Color", required=True, help="Choose a color")
