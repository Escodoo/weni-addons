# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Hr Custom',
    'summary': """
        Weni HR Custom""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://github.com/Escodoo/weni-addons',
    'depends': [
        'hr',
    ],
    'data': [
        'security/weni_hr_employee_gender.xml',
        'views/weni_hr_employee_gender.xml',
        'security/weni_hr_employee_sexual_orientation.xml',
        'views/weni_hr_employee_sexual_orientation.xml',
        'security/weni_hr_employee_shirt_size.xml',
        'views/weni_hr_employee_shirt_size.xml',
        'views/hr_employee.xml',
        'security/weni_hr_employee_seniority.xml',
        'views/weni_hr_employee_seniority.xml',
    ],
    'demo': [
    ],
}
