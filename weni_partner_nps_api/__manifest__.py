# Copyright 2022 - TODAY, Escodoo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Weni Partner Rest Api",
    "summary": """
        Rest API for Partner NPS Management""",
    'version': '12.0.1.0.0',
    "license": "LGPL-3",
    "author": "Escodoo",
    "maintainers": ["marcelsavegnago"],
    "website": "https://github.com/Escodoo/weni_addons",
    "depends": [
        'weni_platform_integration',
        "weni_partner_nps",
        "weni_contacts_custom",
        "base_rest",
        "base_jsonify",
        "base_rest_datamodel",
        "component",
        "auth_api_key",
    ],
    "data": [],
    "demo": ["demo/auth_api_key_demo.xml"],
    "external_dependencies": {"python": ["jsondiff", "marshmallow"]},
    "installable": True,
}
