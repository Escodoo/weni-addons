# Copyright 2021 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Weni Project Custom",
    "summary": """
        Weni Project Custom""",
    "version": "12.0.3.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/weni-addons",
    "depends": ["project", "web_widget_color"],
    "data": [
        "security/project_task_kanban_state.xml",
        "views/assets.xml",
        "views/project_task_kanban_state.xml",
        "views/project_task.xml",
        "views/project_project.xml",
        "views/res_partner.xml",
    ],
    "qweb": [
        "static/src/xml/base.xml",
    ],
    "demo": [],
}
