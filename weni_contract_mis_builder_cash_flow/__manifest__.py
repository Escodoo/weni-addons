# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Contract Mis Builder Cash Flow',
    'summary': """
        Weni Contract Mis Builder Cash Flow""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://www.escodoo.com.br',
    'depends': [
        'mis_builder_cash_flow',
        'contract',
        'queue_job',
    ],
    'data': [
        'views/res_config_settings.xml',
        'views/res_company.xml',
        'views/mis_cash_flow_forecast_line.xml',
        'data/contract_forecast_line_cron.xml',
    ],
    'demo': [
    ],
}
