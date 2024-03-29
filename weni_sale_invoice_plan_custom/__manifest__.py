# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Weni Sale Invoice Plan Custom",
    "summary": """
        WENI - Module customization OCA/sale_workflow/sale_invoice_plan""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "maintainers": ["marcelsavegnago"],
    "development_status": "Alpha",
    "website": "https://github.com/Escodoo/weni-addons",
    "depends": [
        "sale_invoice_plan",
        "project_stage_closed",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "views/sale_invoice_plan.xml",
        "views/sale_order.xml",
    ],
    "demo": [],
}
