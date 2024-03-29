# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Weni Contract Consumption",
    "summary": """
        Weni Contract Custom""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/weni-addons",
    "depends": [
        "sale_management",
        "l10n_br_contract",
    ],
    "data": [
        "security/weni_product_usage.xml",
        "views/weni_product_usage.xml",
        "views/contract_contract.xml",
        "security/contract_line_consumption.xml",
        "views/contract_line_consumption.xml",
    ],
    "demo": [
        "demo/weni_product_usage_demo.xml",
    ],
}
