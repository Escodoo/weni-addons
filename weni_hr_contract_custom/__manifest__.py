# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Hr Contract Custom',
    'summary': """
        Weni HR Contract Custom""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://github.com/Escodoo/weni-addons',
    'depends': [
        'hr_contract',
    ],
    'data': [
        'security/weni_hr_contract_benefit_template.xml',
        'views/weni_hr_contract_benefit_template.xml',
        'security/weni_hr_contract_benefit.xml',
        'views/weni_hr_contract_benefit.xml',
        'views/hr_contract.xml',
    ],
    'demo': [
    ],
}
