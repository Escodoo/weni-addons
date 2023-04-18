from datetime import date

from odoo.tests import common


class TestMisCashFlowForecastLine(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.company = self.env["res.company"].create({"name": "TEST"})
        self.account = self.env["account.account"].create(
            {
                "company_id": self.company.id,
                "code": "TEST3",
                "name": "Test Receivable Account",
                "user_type_id": self.browse_ref(
                    "account.data_account_type_receivable"
                ).id,
                "reconcile": True,
            }
        )
        self.mis_cash_flow_forecast_line = self.env["mis.cash_flow.forecast_line"]
        self.ir_model = self.env["ir.model"]
        self.account_analytic_account = self.env["account.analytic.account"]
        self.res_model = self.ir_model.search([("model", "=", "res.partner")], limit=1)
        self.parent_res_model = self.ir_model.search(
            [("model", "=", "res.users")], limit=1
        )
        self.analytic_account = self.account_analytic_account.create(
            {"name": "Test Analytic Account"}
        )

    def test_action_open_document_related(self):
        partner = self.env.ref("base.res_partner_1")
        forecast_line = self.mis_cash_flow_forecast_line.create(
            {
                "name": "Test Forecast Line 1",
                "res_id": partner.id,
                "res_model_id": self.res_model.id,
                "account_id": self.account.id,
                "analytic_account_id": self.analytic_account.id,
                "date": date.today(),
                "balance": 100,
                "company_id": self.company.id,
            }
        )
        action = forecast_line.action_open_document_related()
        self.assertTrue(action, "Action should be returned.")
        self.assertEqual(
            action.get("res_id"), partner.id, "Partner ID should be the same."
        )

    def test_action_open_parent_document_related(self):
        user = self.env.ref("base.user_demo")
        forecast_line = self.mis_cash_flow_forecast_line.create(
            {
                "name": "Test Forecast Line 1",
                "parent_res_id": user.id,
                "parent_res_model_id": self.parent_res_model.id,
                "account_id": self.account.id,
                "analytic_account_id": self.analytic_account.id,
                "date": date.today(),
                "balance": 100,
                "company_id": self.company.id,
            }
        )
        action = forecast_line.action_open_parent_document_related()
        self.assertTrue(action, "Action should be returned.")
        self.assertEqual(action.get("res_id"), user.id, "User ID should be the same.")
