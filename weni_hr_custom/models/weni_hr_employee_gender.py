# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniHrEmployeeGender(models.Model):

    _name = "weni.hr.employee.gender"
    _description = "Employee Gender"
    _order = 'sequence'

    sequence = fields.Integer(name='Sequence', required=True)
    name = fields.Char(name='Name', required=True, translate=True)
