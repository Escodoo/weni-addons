# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    weni_seniority_id = fields.Many2one(
        comodel_name="weni.hr.employee.seniority",
        string='Seniority'
    )
    weni_level = fields.Integer(string="Level")

    weni_date_last_progression = fields.Date(string="Date of Last Progression")

    weni_key_outcome_job_salary_plan = fields.Text(string="Key outcome of the job and salary plan")

    weni_is_leader = fields.Boolean(string="Is Leader", default=False)

    weni_shirt_size_id = fields.Many2one(
        comodel_name="weni.hr.employee.shirt.size",
        string="Shirt Size"
    )

    weni_sexual_orientation_id = fields.Many2one(
        comodel_name="weni.hr.employee.sexual.orientation",
        string="Sexual Orientation"
    )
    weni_gender_id = fields.Many2one(
        comodel_name="weni.hr.employee.gender",
        string="Gender"
    )

    weni_is_first_job = fields.Boolean(string="Is first job?" , default=False)
