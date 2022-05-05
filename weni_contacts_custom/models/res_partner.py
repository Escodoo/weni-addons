# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date
from odoo import _, api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    weni_customer_size = fields.Selection(
        string='Customer Size',
        selection=([
            ('micro','Micro'),
            ('small','Small'),
            ('medium','Medium'),
            ('large','Large')
        ])
    )

    weni_type_of_service = fields.Selection(
        string="Type of Service",
        selection=([
            ('low','Low'),
            ('medium','Medium'),
            ('high','High')
        ])
    )

    weni_cs_analyst_id = fields.Many2one(
        comodel_name='res.user',
        string='CS Analyst',
    )

    weni_service_analyst_id = fields.Many2one(
        comodel_name='res.user',
        string='Service Analyst',
    )

    weni_customer_at_risk = fields.Boolean(
        string='Customer at risk'
    )

    weni_customer_status = fields.Selection(
        string='Customer Status',
        selection=([
            ('active','Active'),
            ('churn','Churn')
        ])
    )

    weni_churn_request_date = fields.Date(
        string='Churn request date'
    )

    weni_months_customer_lifetime = fields.Integer(
        string='Months of customer lifetime',
        compute='_compute_months_customer_lifetime',
        store=True
    )

    @api.multi
    @api.depends('commercial_partner_id',
                 'commercial_partner_id.child_ids',
                 'commercial_partner_id.invoice_ids',
                 'commercial_partner_id.invoice_ids.state',
                 'commercial_partner_id.child_ids.invoice_ids',
                 'commercial_partner_id.child_ids.invoice_ids.state')
    def _compute_months_customer_lifetime(self):
        for rec in self:
            num_months = 0
            if rec.company_type == 'company' and rec.customer:
                invoice_date = rec.sudo().search_date_first_invoice()
                if invoice_date and invoice_date < date.today():
                    end_date = date.today()
                    start_date = invoice_date
                    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            rec.weni_months_customer_lifetime = num_months

    def search_date_first_invoice(self):
        invoice_date = False
        invoice_ids = (
                self.commercial_partner_id.invoice_ids +
                self.commercial_partner_id.mapped(
                    'child_ids.invoice_ids'))
        if len(invoice_ids) > 0:
            invoice_ids = invoice_ids.filtered(lambda x: x.state == 'open' and x.type == 'out_invoice')
            if len(invoice_ids) > 0:
                invoice_id = invoice_ids.sorted(key=lambda r: r.date_invoice)[0]
                invoice_date = invoice_id.date_invoice
        return invoice_date
