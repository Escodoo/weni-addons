# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WeniHrEmployeeShirtSize(models.Model):

    _name = "weni.hr.employee.shirt.size"
    _description = "Employee Shirt Size"
    _order = 'sequence'

    sequence = fields.Integer(name='Sequence', required=True)
    name = fields.Char()
