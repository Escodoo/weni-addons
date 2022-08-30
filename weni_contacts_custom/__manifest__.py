# Copyright 2022 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Weni Contacts Custom",
    "summary": """
        WENI Contacts Custom""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/weni-addons",
    "depends": [
        "partner_industry_secondary",
        "account",
        "sales_team",
    ],
    "data": [
        "security/weni_customer_mrr_scale.xml",
        "views/weni_customer_mrr_scale.xml",
        "security/weni_customer_service_type.xml",
        "views/weni_customer_service_type.xml",
        "security/weni_customer_status.xml",
        "views/weni_customer_status.xml",
        "views/res_partner.xml",
    ],
    "demo": [],
}
