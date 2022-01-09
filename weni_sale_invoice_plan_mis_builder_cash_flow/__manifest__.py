# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Sale Invoice Plan Mis Builder Cash Flow',
    'summary': """
        Weni Sale Invoice Plan Mis Builder Cash Flow""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'maintainers': ['marcelsavegnago'],
    'website': 'https://www.escodoo.com.br',
    'depends': [
        'mis_builder_cash_flow',
        'sale_invoice_plan',
        'queue_job',
    ],
    'data': [
        'views/res_config_settings.xml',
        'views/res_company.xml',
        'views/mis_cash_flow_forecast_line.xml',
        'data/sale_invoice_plan_forecast_line_cron.xml',
    ],
    'demo': [
    ],
}