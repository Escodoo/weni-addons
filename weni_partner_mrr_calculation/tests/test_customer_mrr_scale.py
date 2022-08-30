from odoo.tests import SavepointCase


class TestMrrScale(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mrr_scale = cls.env["weni.customer.mrr.scale"]

        cls.mrr = mrr_scale.create(
            {
                "name": "Test Partner",
                "company_id": cls.env.user.company_id.id,
                "min_value": 50.00,
                "max_value": 1000.00,
            }
        )
        cls.amount = 0

    def test_mrr_limits(self):
        self.amount = 700.00
        self.assertTrue(
            self.mrr.search(
                [("min_value", "<=", self.amount), ("max_value", ">=", self.amount)],
                limit=1,
            ),
            "MRR: Should return true for value between limits.",
        )

        self.amount = 1200.00
        self.assertFalse(
            self.mrr.search(
                [("min_value", "<=", self.amount), ("max_value", ">=", self.amount)],
                limit=1,
            ),
            "MRR: Should return false for value above upper limit.",
        )

        self.amount = 40.00
        self.assertFalse(
            self.mrr.search(
                [("min_value", "<=", self.amount), ("max_value", ">=", self.amount)],
                limit=1,
            ),
            "MRR: Should return true for value below lower limit.",
        )
