# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    weni_customer_size = fields.Selection(
        string="Customer Size",
        selection=(
            [
                ("micro", "Micro"),
                ("small", "Small"),
                ("medium", "Medium"),
                ("large", "Large"),
            ]
        ),
    )

    weni_service_type_id = fields.Many2one(
        comodel_name="weni.customer.service.type",
        string="Type of Service",
    )

    weni_cs_analyst_id = fields.Many2one(
        comodel_name="res.users",
        string="CS Analyst",
    )

    weni_service_analyst_id = fields.Many2one(
        comodel_name="res.users",
        string="Service Analyst",
    )

    weni_customer_at_risk = fields.Boolean(string="Customer at risk")

    weni_customer_status_id = fields.Many2one(
        comodel_name="weni.customer.status",
        string="Customer Status",
    )

    weni_customer_mrr_scale_id = fields.Many2one(
        comodel_name="weni.customer.mrr.scale", string="MRR Scale"
    )

    weni_churn_request_date = fields.Date(string="Churn request date")

    weni_months_customer_lifetime = fields.Integer(
        string="Months of customer lifetime",
        compute="_compute_months_customer_lifetime",
        store=True,
    )

    weni_has_dedicate_team = fields.Boolean(string="Has Dedicated Team")

    weni_recurrence_task_ids = fields.One2many(
        comodel_name="res.partner.service.type.task",
        inverse_name="partner_id",
        string="Recurrence Tasks",
        required=False,
        store=True,
    )

    @api.multi
    @api.depends(
        "commercial_partner_id",
        "commercial_partner_id.child_ids",
        "commercial_partner_id.invoice_ids",
        "commercial_partner_id.invoice_ids.state",
        "commercial_partner_id.child_ids.invoice_ids",
        "commercial_partner_id.child_ids.invoice_ids.state",
    )
    def _compute_months_customer_lifetime(self):
        for rec in self:
            num_months = 0
            if rec.company_type == "company" and rec.customer:
                invoice_date = rec.sudo().search_date_first_invoice()
                if invoice_date and invoice_date < date.today():
                    end_date = date.today()
                    start_date = invoice_date
                    num_months = (end_date.year - start_date.year) * 12 + (
                        end_date.month - start_date.month
                    )
            rec.weni_months_customer_lifetime = num_months

    def search_date_first_invoice(self):
        invoice_date = False
        invoice_ids = (
            self.commercial_partner_id.invoice_ids
            + self.commercial_partner_id.mapped("child_ids.invoice_ids")
        )
        if len(invoice_ids) > 0:
            invoice_ids = invoice_ids.filtered(
                lambda x: x.state == "open" and x.type == "out_invoice"
            )
            if len(invoice_ids) > 0:
                invoice_id = invoice_ids.sorted(key=lambda r: r.date_invoice)[0]
                invoice_date = invoice_id.date_invoice
        return invoice_date

    def _cron_generate_recurrence_tasks(self, recurrence_unit=False, delay=0):
        domain = [
            "|",
            ("date_last_recurrence", "<", date.today()),
            ("date_last_recurrence", "=", False),
            ("partner_id.active", "=", True),
            ("date_next_recurrence", "=", date.today() + relativedelta(days=delay)),
        ]

        if recurrence_unit:
            if recurrence_unit == "days":
                domain += {("recurrence_unit", "=", "days")}
            elif recurrence_unit == "weeks":
                domain += {("recurrence_unit", "=", "weeks")}
            elif recurrence_unit == "months":
                domain += {("recurrence_unit", "=", "months")}

        recurrence_tasks = self.env["res.partner.service.type.task"].search(domain)

        for recurrence_task in recurrence_tasks:
            calendar_event = (
                recurrence_task.partner_id._create_recurrence_task_meeting(
                    recurrence_task.name,
                    recurrence_task.user_id,
                    recurrence_task.user_id.partner_id,  # TODO: implementar campo
                    recurrence_task.date_next_recurrence,
                    recurrence_task.date_next_recurrence,
                ).id
                if (recurrence_task.activity_type_id.category == "meeting")
                else False
            )

            recurrence_task.partner_id.activity_schedule(
                user_id=recurrence_task.user_id.id,
                activity_type_id=recurrence_task.activity_type_id.id,
                date_deadline=recurrence_task.date_next_recurrence,
                summary=recurrence_task.name,
                note=recurrence_task.note,
                calendar_event_id=calendar_event,
            )

            recurrence_task.date_last_recurrence = date.today() + relativedelta(
                days=delay
            )

    def _create_recurrence_tasks(self, service_type):
        fields = self.env["weni.customer.service.type.task.mixin"]._fields.keys()
        for rec in self:
            rec.weni_recurrence_task_ids.filtered(lambda t: t.template_task_id).unlink()
            for task in service_type.task_ids:
                template_task_id = task.id
                vals = task._convert_to_write(task.read(fields)[0])
                vals.pop("id", None)
                vals.update({"partner_id": rec.id})
                vals.update({"template_task_id": template_task_id})
                rec.weni_recurrence_task_ids.create(vals)

    @api.multi
    def write(self, vals):
        if "weni_service_type_id" in vals:
            if vals.get("weni_service_type_id"):
                for rec in self:
                    service_type = self.env["weni.customer.service.type"].browse(
                        vals.get("weni_service_type_id")
                    )
                    rec._create_recurrence_tasks(service_type)
            else:
                for rec in self:
                    rec.weni_recurrence_task_ids.filtered(
                        lambda t: t.template_task_id
                    ).unlink()
        return super().write(vals)

    def _create_recurrence_task_meeting(self, name, user, attendees, start, stop):
        start_time = datetime.min.time()
        values = {}
        values["name"] = name
        values["allday"] = True
        values["partner_ids"] = [(4, partner.id) for partner in attendees]
        values["partner_id"] = user.id
        values["user_id"] = user.id
        values["start"] = start
        values["stop"] = stop
        # values['activity_ids'] = [(4, activity.id)]
        meeting = self.env["calendar.event"].create(values)
        meeting.start_datetime = datetime.combine(start, start_time)
        return meeting
