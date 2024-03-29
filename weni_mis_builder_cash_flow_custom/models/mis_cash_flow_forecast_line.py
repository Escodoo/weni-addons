# Copyright 2021 - TODAY, Marcel Savegnago
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MisCashFlowForecastLine(models.Model):
    _inherit = "mis.cash_flow.forecast_line"

    res_id = fields.Integer(string="Resource ID")
    res_model_id = fields.Many2one("ir.model", "Document Model", ondelete="cascade")
    res_model = fields.Char(
        "Document Model Name", related="res_model_id.model", readonly=True, store=True
    )
    parent_res_id = fields.Integer(string="Parent Resource ID")
    parent_res_model_id = fields.Many2one(
        "ir.model", "Parent Document Model", ondelete="cascade"
    )
    parent_res_model = fields.Char(
        "Parent Document Model Name",
        related="parent_res_model_id.model",
        readonly=True,
        store=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account", comodel_name="account.analytic.account"
    )
    operational_account_id = fields.Many2one(
        string="Operational Account", comodel_name="account.account"
    )

    def action_open_document_related(self):
        if self.res_model and self.res_id:
            return self.env[self.res_model].browse(self.res_id).get_formview_action()
        return False

    def action_open_parent_document_related(self):
        if self.parent_res_model and self.parent_res_id:
            return (
                self.env[self.parent_res_model]
                .browse(self.parent_res_id)
                .get_formview_action()
            )
        return False
