# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _compute_mrr(self, amount):
        return self.env["weni.customer.mrr.scale"].search(
            [
                ("min_value", "<=", amount),
                ("max_value", ">=", amount),
            ],
            limit=1,
        )

    @api.model
    def _cron_update_mrr(self):
        partners = self.env["res.partner"].search(
            [("is_company", "=", True), ("active", "=", True)]
        )
        for partner in partners:
            mrr = False
            invoice_ids = (
                partner.commercial_partner_id.invoice_ids
                + partner.commercial_partner_id.mapped("child_ids.invoice_ids")
            )
            if len(invoice_ids) > 0:
                invoice_ids = invoice_ids.filtered(
                    lambda x: (x.state == "open" or x.state == "paid")
                    and x.type == "out_invoice"
                    and x.invoice_line_ids[0].contract_line_id
                    and x.date_invoice > fields.Date.today() - relativedelta(months=3)
                )
                if len(invoice_ids) > 0:
                    invoice_id = invoice_ids.sorted(key=lambda r: r.date_invoice)[-1]
                    mrr = self._compute_mrr(invoice_id.amount_total_company_signed)
            partner.weni_customer_mrr_scale_id = mrr
