# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResPartnerNps(models.Model):

    _name = "res.partner.nps"
    _description = "Res Partner Nps"  # TODO



    name = fields.Char(string='Name', compute='_compute_name')
    submission_date = fields.Date(
        'Submission Date',
        default=fields.Date.context_today, required=True)
    return_date = fields.Date('Return Date')
    channel = fields.Char('Channel', required=True)
    partner_id = fields.Many2one('res.partner', 'Company', required=True)
    contact_id = fields.Many2one('res.partner', 'Contact', required=True)
    nps = fields.Integer('NPS')
    comment = fields.Text('Comment', placeholder='Customer comment...')

    @api.depends("submission_date", "partner_id", "contact_id")
    def _compute_name(self):
        locale = self.env.context.get("lang") or self.env.user.lang or "en_US"
        for rec in self:
            if not rec.partner_id or not rec.contact_id:
                rec.name = "Draft"
            else:
                rec.name = _("%s / %s / %s") % (
                    rec.submission_date,
                    rec.partner_id.name,
                    rec.contact_id.name
                )
