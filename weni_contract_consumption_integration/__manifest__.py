# Copyright 2022 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Contract Consumption Integration',
    'summary': """
        Weni Contract Consumption Integration""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://github.com/escodoo/weni-addons',
    'depends': [
        'weni_contract_consumption'
    ],
    'data': [
        'views/res_partner.xml',
        'views/contract_line_consumption.xml',
        'data/contract_consumption_integration_cron.xml',
    ],
    'demo': [
    ],
}
