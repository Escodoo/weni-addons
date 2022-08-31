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

    def test_mrr_limits(self):
        self.assertTrue(
            self.mrr._compute_mrr(700),
            "MRR: Should return true for value between limits.",
        )

        self.assertFalse(
            self.mrr._compute_mrr(1200),
            "MRR: Should return false for value above upper limit.",
        )

        self.assertFalse(
            self.mrr._compute_mrr(40),
            "MRR: Should return true for value below lower limit.",
        )
