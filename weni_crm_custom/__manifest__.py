# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Crm Custom',
    'description': """
        Customizações do Modulo CRM - Weni""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://www.escodoo.com.br',
    'depends': [
        'crm',
        'crm_secondary_salesperson'
    ],
    'data': [
        'security/crm_lead_decision_maker.xml',
        'views/crm_lead_decision_maker.xml',
        'security/crm_lead_channel.xml',
        'views/crm_lead_channel.xml',
        'views/crm_lead.xml',
    ],
    'demo': [
    ],
}
