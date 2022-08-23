# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    @api.depends("weni_nps_ids")
    def _compute_weni_nps_count(self):
        for rec in self:
            rec.weni_nps_count = len(rec.weni_nps_ids)

    @api.depends("weni_current_nps")
    def _compute_current_nps_classification(self):

        for rec in self:
            if rec.weni_nps_ids:
                if rec.weni_current_nps <= 3:
                    rec.weni_current_nps_classification = "danger"
                elif rec.weni_current_nps > 3 and rec.weni_current_nps <= 6:
                    rec.weni_current_nps_classification = "alert"
                elif rec.weni_current_nps > 6:
                    rec.weni_current_nps_classification = "success"
                else:
                    rec.weni_current_nps_classification = False
            else:
                rec.weni_current_nps_classification = False

    weni_current_nps = fields.Integer(
        compute="_compute_partner_nps", string=" NPS", store=True
    )
    weni_nps_ids = fields.One2many("res.partner.nps", "partner_id", "NPSs")
    weni_nps_count = fields.Integer(
        compute=_compute_weni_nps_count,
        string="Number of NPSs",
    )

    @api.depends("weni_nps_ids")
    def _compute_partner_nps(self):
        for rec in self:
            nps_record = self.env["res.partner.nps"].search(
                [("partner_id", "=", rec.id), ("return_date", "!=", False)],
                order="submission_date desc, nps asc",
                limit=1,
            )

            rec.weni_current_nps = nps_record.nps
            # # TODO: Precisa alinhar com o cliente se isto de fato é necessário
            # rec._compute_current_nps_classification()

    def action_view_weni_npss(self):
        action = self.env.ref("weni_partner_nps.res_partner_nps_act_window").read()[0]
        if self.weni_nps_count > 1:
            action["domain"] = [("id", "in", self.weni_nps_ids.ids)]
        else:
            action["views"] = [
                (self.env.ref("weni_partner_nps.res_partner_nps_form_view").id, "form")
            ]
            action["res_id"] = self.weni_nps_ids and self.weni_nps_ids.ids[0] or False
        return action
