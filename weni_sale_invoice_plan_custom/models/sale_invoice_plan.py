# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleInvoicePlan(models.Model):

    _inherit = "sale.invoice.plan"

    description = fields.Char(
        string="Description",
    )

    project_id = fields.Many2one(
        "project.project", "Project", help="Sale Invoice Plan Project"
    )

    project_task_ids = fields.Many2many(
        comodel_name="project.task",
        string="Project Task",
        copy=False,
    )

    @api.onchange("project_id")
    def _onchange_project_id(self):
        self.project_task_ids = False

    @api.multi
    def write(self, vals):
        for line in self:
            if line.invoiced:
                raise UserError(
                    _(
                        "This row already has an invoice created and therefore"
                        "cannot be edited."
                    )
                )
        return super(SaleInvoicePlan, self).write(vals)
