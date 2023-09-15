# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Project Project Sla',
    'summary': """
        WENI Project Project SLA""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://github.com/Escodoo/weni-addons',
    'depends': [
        "project_status"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_project.xml',
        'views/project_project_sla.xml',
        'views/project_project_sla_line.xml',
        # 'data/ir_cron_data.xml',
    ],
}
