# Copyright 2022 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Weni Partner MRR Calculation",
    "summary": """
        WENI Partner MRR Calculation""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/weni-addons",
    "depends": [
        "weni_contacts_custom",
        "sale_commercial_partner",
        "account",
        "contract",
    ],
    "data": [
        "data/weni_mrr_cron.xml",
        "views/weni_customer_mrr_scale.xml",
    ],
}
