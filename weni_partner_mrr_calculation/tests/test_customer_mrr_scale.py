from odoo.tests import SavepointCase


class TestMrrScale(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mrr_scale = cls.env["weni.customer.mrr.scale"]
        currency = cls.env["res.currency"]
        # cls.env["account.invoice"]
        cls.user_admin = cls.env.ref("base.user_root")
        cls.user_demo = cls.env.ref("base.user_demo")
        cls.user_portal = cls.env.ref("base.demo_user0")

        cls.currency = currency.create(
            {
                "name": "Test currency",
                "symbol": "%$",
            }
        )
        cls.mrr = mrr_scale.create(
            {
                "name": "Test Partner",
                "currency_id": 1,
                "min_value": 50.00,
                "max_value": 1000.00,
            }
        )
        cls.amount = 0

    def test_mrr_name(self):
        self.assertTrue(self.mrr.name, "MRR should have a name.")

    def test_mrr_limits(self):
        self.amount = 700.00
        self.assertTrue(
            self.mrr.check_value(self.amount, self.currency),
            "MRR: Should return true for value between limits.",
        )
        self.amount = 1200.00
        self.assertFalse(
            self.mrr.check_value(self.amount, self.currency),
            "MRR: Should return false for value above upper limit.",
        )
        self.amount = 40.00
        self.assertFalse(
            self.mrr.check_value(self.amount, self.currency),
            "MRR: Should return true for value below lower limit.",
        )
