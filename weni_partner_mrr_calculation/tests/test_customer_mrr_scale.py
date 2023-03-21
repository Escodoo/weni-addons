import datetime
from odoo.tests import common

class TestResPartner(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestResPartner, cls).setUpClass()

        # Criar registros necessários para o teste
        cls.res_partner_obj = cls.env["res.partner"]
        cls.weni_customer_mrr_scale_obj = cls.env["weni.customer.mrr.scale"]
        cls.account_invoice_obj = cls.env["account.invoice"]
        cls.account_invoice_line_obj = cls.env["account.invoice.line"]

        cls.scale_1 = cls.weni_customer_mrr_scale_obj.create({
            "min_value": 0,
            "max_value": 1000,
        })

        cls.scale_2 = cls.weni_customer_mrr_scale_obj.create({
            "min_value": 1001,
            "max_value": 2000,
        })

        cls.partner_1 = cls.res_partner_obj.create({
            "name": "Partner 1",
            "is_company": True,
        })

        cls.partner_2 = cls.res_partner_obj.create({
            "name": "Partner 2",
            "is_company": True,
        })

        cls.invoice_1 = cls.account_invoice_obj.create({
            "partner_id": cls.partner_1.id,
            "date_invoice": datetime.date.today() - datetime.timedelta(days=10),
            "type": "out_invoice",
            "state": "open",
        })

        cls.invoice_line_1 = cls.account_invoice_line_obj.create({
            "invoice_id": cls.invoice_1.id,
            "name": "Invoice Line 1",
            "price_unit": 500,
            "quantity": 1,
        })

        cls.invoice_2 = cls.account_invoice_obj.create({
            "partner_id": cls.partner_2.id,
            "date_invoice": datetime.date.today() - datetime.timedelta(days=15),
            "type": "out_invoice",
            "state": "open",
        })

        cls.invoice_line_2 = cls.account_invoice_line_obj.create({
            "invoice_id": cls.invoice_2.id,
            "name": "Invoice Line 2",
            "price_unit": 1500,
            "quantity": 1,
        })

    def test_compute_mrr(self):
        # Testando a função _compute_mrr com um valor dentro da escala_1
        result_1 = self.res_partner_obj._compute_mrr(500)
        self.assertEqual(result_1, self.scale_1, "A escala MRR calculada está incorreta.")

        # Testando a função _compute_mrr com um valor dentro da escala_2
        result_2 = self.res_partner_obj._compute_mrr(1500)
        self.assertEqual(result_2, self.scale_2, "A escala MRR calculada está incorreta.")

    def test_cron_update_mrr(self):
        # Executando a função _cron_update_mrr
        self.res_partner_obj._cron_update_mrr()

        # Verificar se a escala MRR foi atualizada corretamente
        self.assertEqual(self.partner_1.weni_customer_mrr_scale_id, self.scale_1, "A escala MRR não foi atualizada corretamente.")
        self.assertEqual(self.partner_2.weni_customer_mrr_scale_id, self.scale_2, "A escala MRR não foi atualizada corretamente.")
