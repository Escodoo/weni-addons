from odoo.tests import SavepointCase


class TestMrrScale(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mrr_scale = cls.env["weni.customer.mrr.scale"]
        cls.currency_id = cls.env.ref("base.USD").id
        cls.user_admin = cls.env.ref("base.user_root")
        cls.user_demo = cls.env.ref("base.user_demo")
        cls.user_portal = cls.env.ref("base.demo_user0")

        cls.mrr = mrr_scale.create(
            {
                "name": "Test Partner",
                "currency_id": 1,
                "min_value": 50.00,
                "max_value": 1000.00,
            }
        )
        cls.account_type = cls.env["account.account.type"].create(
            {
                "name": "Test",
                "type": "receivable",
            }
        )
        cls.account = cls.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TEST",
                "user_type_id": cls.account_type.id,
                "reconcile": True,
            }
        )
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Mr. Odoo",
            }
        )
        cls.partner_2 = cls.env["res.partner"].create(
            {
                "name": "Mrs. Odoo",
            }
        )
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "NO TAX",
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "amount": 0,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Test purchase journal",
                "code": "TPUR",
                "type": "purchase",
            }
        )
        cls.invoice = cls.env["account.invoice"].create(
            {
                "name": "Test Customer Invoice",
                "journal_id": cls.journal.id,
                "partner_id": cls.partner_1.id,
                "account_id": cls.account.id,
                "type": "in_invoice",
            }
        )
        cls.invoice_line = cls.env["account.invoice.line"]
        cls.invoice_line1 = cls.invoice_line.create(
            {
                "invoice_id": cls.invoice.id,
                "name": "Line 1",
                "price_unit": 200.00,
                "account_id": cls.account.id,
                "invoice_line_tax_ids": [(6, 0, [cls.tax.id])],
                "quantity": 1,
            }
        )
        cls.invoice._onchange_invoice_line_ids()

    def test_mrr_name(self):
        self.assertTrue(self.mrr.name, "MRR should have a name.")

    def test_mrr_limits(self):
        self.assertEqual(self.invoice.amount_total, 200.00)
        self.assertTrue(
            self.mrr.check_value(self.invoice.amount_total, self.currency_id),
            "MRR: Should return true for value between limits.",
        )
        self.invoice_line1.price_unit = 1200
        self.invoice._onchange_invoice_line_ids()
        self.assertFalse(
            self.mrr.check_value(self.invoice.amount_total, self.currency_id),
            "MRR: Should return false for value above upper limit.",
        )
        self.invoice_line1.price_unit = 40
        self.invoice._onchange_invoice_line_ids()
        self.assertFalse(
            self.mrr.check_value(self.invoice.amount_total, self.currency_id),
            "MRR: Should return true for value below lower limit.",
        )
