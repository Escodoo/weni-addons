# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.osv import expression


class ProjectProject(models.Model):

    _inherit = "project.project"
    
    use_sla = fields.Boolean(string="Use SLA")
    resource_calendar_id = fields.Many2one(
        "resource.calendar",
        "Working Hours",
        default=lambda self: self.env.user.company_id.resource_calendar_id,
    )

    sla_ids = fields.Many2many(
        comodel_name="project.project.sla",
        string="Computed SLAs",
        compute="_compute_sla_ids",
        store=True,
    )
    sla_line_ids = fields.One2many(
        comodel_name="project.project.sla.line", inverse_name="project_id", string="SLA Lines"
    )
    sla_deadline = fields.Datetime(
        string="Highest SLA Deadline",
        readonly=True,
        compute="_compute_sla_deadline",
        store=True,
    )

    def write(self, vals):
        # SLA business
        sla_triggers = self._sla_reset_trigger()
        if any(field_name in sla_triggers for field_name in vals.keys()):
            any_reached = self.sla_line_ids.filtered(lambda x: x.reached_date)
            if not any_reached:
                self.sudo().sla_line_ids.unlink()
        return super().write(vals)

    @api.depends("partner_id")
    def _compute_sla_ids(self):
        sla_per_tasks = self._sla_find()
        for tasks, slas in sla_per_tasks.items():
            tasks.sla_ids = slas

    @api.depends("create_date", "sla_line_ids", "sla_line_ids.deadline")
    def _compute_sla_deadline(self):
        for task in self:
            task.calculate_sla_deadline()

    def calculate_sla_deadline(self):
        if (
            not self.create_date
            or not self.resource_calendar_id
            or not self.sla_line_ids
        ):
            return
        sla_line_ids = self.sla_line_ids.sorted(key=lambda p: p.deadline, reverse=True)
        self.sla_deadline = sla_line_ids[0].deadline

    def update_unmet_sla_lines(self):
        sla_lines = []
        for sla_line in self.sla_line_ids:
            if not sla_line.reached_date and sla_line.status == "not_met":
                calendar = self.resource_calendar_id
                start_date = self.create_date
                sla = sla_line.sla_id
                duration = sla.duration
                work_days_data = calendar.plan_hours(
                    duration, start_date, compute_leaves=True
                )
                new_deadline = work_days_data
                sla_lines.append(
                    (1, sla_line.id, {"status": "not_met", "deadline": new_deadline})
                )
                sla_lines.append(
                    (
                        1,
                        sla_line.id,
                        {
                            "sla_id": sla.id,
                            "status": "not_met",
                            "create_date": sla_line.create_date,
                            "write_date": sla_line.write_date,
                            "task_id": sla_line.task_id.id,
                            "id": False,
                            "deadline": new_deadline,
                        },
                    )
                )
        if sla_lines:
            self.write({"sla_line_ids": sla_lines})

    def _create_sla_lines(self):
        sla_lines = []
        for sla in self.sla_ids:
            sla_deadline = self.resource_calendar_id.plan_hours(
                sla.duration, self.create_date, compute_leaves=True
            )
            sla_lines.append(
                (
                    0,
                    0,
                    {"sla_id": sla.id, "status": "not_met", "deadline": sla_deadline},
                )
            )
        self.write({"sla_line_ids": sla_lines})

    @api.model
    def _update_sla_lines(self):
        now = fields.Datetime.now()
        sla_lines = []
        self.update_unmet_sla_lines()
        for sla_line in self.sla_line_ids:
            if (
                self.stage_id.id == sla_line.sla_id.target_stage_id.id
                and not sla_line.reached_date
            ):
                sla_line.reached_date = now
            sla_deadline = self.resource_calendar_id.plan_hours(
                sla_line.sla_id.duration, self.create_date, compute_leaves=True
            )
            if (now <= sla_deadline and not sla_line.reached_date) or (
                sla_line.reached_date and sla_line.reached_date > sla_deadline
            ):
                sla_line.status = "not_met"

            if (sla_line.reached_date and sla_line.reached_date < sla_deadline):
                sla_line.status = "met"
            sla_lines.append(
                (
                    1,
                    sla_line.id,
                    {"status": sla_line.status, "reached_date": sla_line.reached_date},
                )
            )
        self.write({"sla_line_ids": sla_lines})

    def _sla_find_extra_domain(self):
        self.ensure_one()
        return [
            "|",
            "|",
            ("partner_ids", "parent_of", self.partner_id.ids),
            ("partner_ids", "child_of", self.partner_id.ids),
            ("partner_ids", "=", False),
        ]

    @api.model
    def _sla_reset_trigger(self):
        return ["partner_id"]

    def _sla_find(self):
        records_map = {}
        sla_domain_map = {}

        def _generate_key(record):
            fields_list = record._sla_reset_trigger()
            key = []
            for field_name in fields_list:
                if record._fields[field_name].type == "many2one":
                    key.append(record[field_name].id)
                else:
                    key.append(record[field_name])
            return tuple(key)

        for record in self:
            if record.use_sla:
                key = _generate_key(record)
                records_map.setdefault(key, self.env["project.project"])
                records_map[key] |= record
                if key not in sla_domain_map:
                    sla_domain_map[key] = expression.AND(
                        [
                            [
                                ("id", "=", record.id),
                            ],
                            record._sla_find_extra_domain(),
                        ]
                    )

        result = {}
        for key, tasks in records_map.items():
            domain = sla_domain_map[key]
            slas = self.env["project.project.sla"].search(domain)
            result[tasks] = slas.filtered(
                lambda s: not s.tag_ids or (tasks.tag_ids & s.tag_ids)
            )
        return result

    def _sync_sla_lines(self):
        if not self.sla_line_ids:
            self._create_sla_lines()
        else:
            self._update_sla_lines()

    @api.model
    def _sync_all_sla_lines(self):
        records = (
            self.env["project.project"]
            .search([])
            .filtered(
                lambda r: (
                    r.active
                    and r.use_sla
                    and r.create_date >= r.start_date_sla
                    and (
                        any(not p.reached_date for p in r.sla_line_ids)
                        or not r.sla_line_ids)
                )
            )
        )
        for record in records:
            self._sync_sla_lines()

    @api.model
    def cron_sync_all_sla_lines(self):
        self._sync_all_sla_lines()