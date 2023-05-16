# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2.extensions import AsIs

from odoo import api, fields, models, tools


class AccountMoveLineForecast(models.Model):
    _name = "account.move.line.forecast"
    _description = "Account Move Line Forecast"
    _auto = False

    line_type = fields.Selection(
        [("forecast_line", "Forecast Line"), ("move_line", "Journal Item")],
        index=True,
        readonly=True,
    )
    name = fields.Char(
        readonly=True,
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        auto_join=True,
        index=True,
        readonly=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        readonly=True,
    )
    move_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Journal Item",
        auto_join=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        auto_join=True,
        readonly=True,
        index=True,
    )
    credit = fields.Float(
        readonly=True,
    )
    debit = fields.Float(
        readonly=True,
    )
    date = fields.Date(
        readonly=True,
        index=True,
    )
    reconciled = fields.Boolean(
        readonly=True,
    )
    full_reconcile_id = fields.Many2one(
        "account.full.reconcile",
        string="Matching Number",
        readonly=True,
        index=True,
    )
    user_type_id = fields.Many2one(
        "account.account.type",
        auto_join=True,
        readonly=True,
        index=True,
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        auto_join=True,
        readonly=True,
        index=True,
    )

    @api.model_cr
    def init(self):
        query = """
            SELECT
                -- we use negative id to avoid duplicates and we don't use
                -- ROW_NUMBER() because the performance was very poor
                -aml.id as id,
                CAST('move_line' AS varchar) as line_type,
                aml.id as move_line_id,
                aml.account_id as account_id,
                aml.analytic_account_id as analytic_account_id,
                aml.debit AS debit,
                aml.credit AS credit,
                aml.reconciled as reconciled,
                aml.full_reconcile_id as full_reconcile_id,
                aml.partner_id as partner_id,
                aml.company_id as company_id,
                aml.user_type_id as user_type_id,
                aml.name as name,
                aml.date_maturity as date
            FROM account_move_line as aml
            UNION ALL
            SELECT
                fl.id as id,
                CAST('forecast_line' AS varchar) as line_type,
                Null as move_line_id,
                fl.operational_account_id as account_id,
                fl.analytic_account_id as analytic_account_id,
                CASE
                    WHEN fl.balance < 0
                    THEN -fl.balance
                    ELSE 0.0
                END AS debit,
                CASE
                    WHEN fl.balance > 0
                    THEN fl.balance
                    ELSE 0.0
                END AS credit,
                Null as reconciled,
                Null as full_reconcile_id,
                fl.partner_id as partner_id,
                fl.company_id as company_id,
                account.user_type_id as user_type_id,
                fl.name as name,
                fl.date as date
            FROM mis_cash_flow_forecast_line AS fl
            INNER JOIN account_account AS account
            ON account.id = fl.operational_account_id
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self._cr.execute(
            "CREATE OR REPLACE VIEW %s AS %s", (AsIs(self._table), AsIs(query))
        )

    @api.multi
    def action_open_related_line(self):
        self.ensure_one()
        if self.line_type == "move_line":
            return self.move_line_id.get_formview_action()
        else:
            return (
                self.env["mis.cash_flow.forecast_line"]
                .browse(self.id)
                .get_formview_action()
            )
