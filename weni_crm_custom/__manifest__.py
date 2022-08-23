# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Weni Crm Custom",
    "summary": """
        Customizações do Modulo CRM - Weni""",
    "version": "12.0.2.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/weni-addons",
    "depends": [
        "l10n_br_crm",
        "crm_secondary_salesperson",
        "crm_industry",
    ],
    "data": [
        "security/crm_lead_user.xml",
        "views/crm_lead_user.xml",
        "security/crm_lead_decision_maker.xml",
        "views/crm_lead_decision_maker.xml",
        "security/crm_lead_channel.xml",
        "views/crm_lead_channel.xml",
        "views/crm_lead.xml",
    ],
    "demo": [],
}
