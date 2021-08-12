# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Contract Consumption',
    'description': """
        Weni Contract Custom""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://www.escodoo.com.br',
    'depends': [
        'product_contract',
    ],
    'data': [
        'views/contract_contract.xml',
        'views/product_template.xml',
        'security/contract_line_consumption.xml',
        'views/contract_line_consumption.xml',
    ],
}
