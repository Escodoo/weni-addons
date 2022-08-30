# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    project_ids = fields.One2many("project.project", "partner_id", string="Projects")
    project_count = fields.Integer(
        compute="_compute_project_count", string="# Projects"
    )

    def _compute_project_count(self):
        fetch_data = self.env["project.project"].read_group(
            [("partner_id", "in", self.ids)], ["partner_id"], ["partner_id"]
        )
        result = {
            data["partner_id"][0]: data["partner_id_count"] for data in fetch_data
        }
        for partner in self:
            partner.project_count = result.get(partner.id, 0)
