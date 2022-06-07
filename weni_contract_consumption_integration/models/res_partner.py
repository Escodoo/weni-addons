# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import requests
from datetime import date, timedelta
from odoo import _, api, fields, models, tools

_logger = logging.getLogger(__name__)

def weni_consumption_find(search, apikey=False):
    if not search:
        return None

    if not apikey:
        _logger.error('''[WENI_INTEGRATION] API key for Weni required.\n
                          Save this key in System Parameters with key: weni.api_key_weni, value: <your api key>
                          Visit ... for more information.
                          ''')
        return None

    url = "https://api.weni.ai/v1/organization/org/grpc/contact-active/" + search

    try:
        result = requests.get(url, headers={'Authorization': apikey}).json()
    except:
        _logger.error('[WENI_INTEGRATION] Cannot contact weni servers. Please make sure that your Internet connection is up and running.')
        return None

    try:
        if result['projects']:
            _logger.info('[WENI INTEGRATION] Finished get active users by search: %s', search)
    except:
        if 'detail' in result:
            _logger.error('[WENI INTEGRATION] %s: %s', result['detail'],search)
        else:
            _logger.error('[WENI INTEGRATION] Unable to collect active users by search: %s', search)
        # _logger.debug("Traceback:", exc_info=True)
    return result

def weni_contract_consumption_query_data(weni_id=None, after=None, before=None):
    return (weni_id + '/?after=' + after + '&before=' + before)


class ResPartner(models.Model):

    _inherit = "res.partner"

    @classmethod
    def _weni_consumption_localize(cls, apikey, weni_id='', after='', before=''):
        search = weni_contract_consumption_query_data(weni_id=weni_id, after=after, before=before)
        result = weni_consumption_find(search, apikey)
        if result is None:
            return None
        return result

    @api.multi
    def weni_consumption_localize(self):
        apikey = self.env['ir.config_parameter'].sudo().get_param('weni.api_key_weni')
        consumption = self.env['contract.line.consumption']
        contract_line = self.env['contract.line']

        # before_date = date.today() - timedelta(days=1)
        # after_date = before_date.replace(day=1)

        before_date = date.today().replace(day=1)
        consumption_date = before_date - timedelta(days=1)
        after_date = consumption_date.replace(day=1) - timedelta(days=1)

        # before_date = date.today()
        # after_date = date.today() - timedelta(days=2)
        # consumption_date = date.today() - timedelta(days=1)

        after_date_formated = after_date.strftime('%Y-%m-%d')
        before_date_formated = before_date.strftime('%Y-%m-%d')

        for rec in self:
            if rec.weni_id:
                result = rec._weni_consumption_localize(apikey,
                                               rec.weni_id,
                                               after_date_formated,
                                               before_date_formated)
                if result and 'projects' in result:
                    for item in result['projects']:
                        uuid = item.get('uuid')
                        contract_line = contract_line.search([('weni_id', '=', uuid)], limit=1)
                        if contract_line:
                            consumption_line_is_invoiced = False
                            for consumption_line in contract_line.contract_line_consumption_ids:
                                if consumption_line.consumption_date == consumption_date:
                                    if consumption_line.invoice_status == 'to_be_invoice':
                                        consumption_line.unlink()
                                    else:
                                        _logger.error('[WENI INTEGRATION] Consumption Line is Invoiced: %s', consumption_line.contract_line_id.name)
                                        consumption_line_is_invoiced = True
                            if not consumption_line_is_invoiced:
                                consumption.create({
                                    'contract_id': contract_line.contract_id.id,
                                    'contract_line_id':contract_line.id,
                                    'consumption_quantity': item.get('active_contacts'),
                                    'consumption_date': consumption_date,
                                    'invoice_status': 'to_be_invoice'
                                })
        return True

    @api.model
    def _cron_weni_consumption_localize(self):
        partners = self.env['res.partner'].search(
            [
               ['contract_ids', '>', 0],
            ]
        )
        for partner in partners:
            if partner.weni_id:
                partner.weni_consumption_localize()
