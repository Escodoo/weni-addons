# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    @api.model
    def _cron_update_mrr(self):
        for rec in self:
            partner = self.env["res.partner"].search(
                [("is_company", "=", True), ("partner_id", "=", rec.id)]
            )
            invoice_ids = (
                partner.commercial_partner_id.invoice_ids
                + partner.commercial_partner_id.mapped("child_ids.invoice_ids")
            )

            if len(invoice_ids) > 0:
                invoice_ids = invoice_ids.filtered(
                    lambda x: (x.state == "open" or x.state == "paid")
                    and x.type == "out_invoice"
                    and x.line.contract_line_id
                )
                if len(invoice_ids) > 0:
                    invoice_id = invoice_ids.sorted(key=lambda r: r.date_invoice)[-1]
                    mrr_ids = self.env["weni.customer.mrr.scale"].search([])

                    for mrr in mrr_ids:
                        if mrr.check_value(
                            invoice_id.amount_total, invoice_id.currency_id
                        ):
                            partner.weni_customer_mrr_scale_id = mrr
                            break
