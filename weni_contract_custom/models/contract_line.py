# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractLine(models.Model):

    _inherit = 'contract.line'

    @api.model
    def cron_create_crm_opportunity_non_renewable_contract(self):
        crm_model = self.env['crm.lead']
        today = fields.Date.context_today(self)
        contract_lines = self.search([
            ('is_auto_renew', '=', False),
            ('date_end', '>', today),
            ('termination_notice_date', '=', today)])
        for line in contract_lines:
            name = (
                    'Renewal: ' +
                    line.contract_id.name + ' - ' + line.name
            )
            opportunity = crm_model.create({
                'name': name,
                'description': line.contract_id.name,
                'partner_id': line.contract_id.partner_id.id,
                'user_id': line.contract_id.user_id.id,
                'planned_revenue': line.price_subtotal,
                'type': 'opportunity',
                'priority': '3',
                'date_deadline': line.date_end,
            })

            opportunity.message_post(body=_(
                'Contract about to expire: '
                '<a href="#" data-oe-model="%s" data-oe-id="%s">Contract'
                '</a><br>'
                'Contract line about to expire: '
                '<a href="#" data-oe-model="%s" data-oe-id="%s">Contract Line'
                '</a>'
            )
            % (line.contract_id._name, line.contract_id.id, line._name, line.id))
