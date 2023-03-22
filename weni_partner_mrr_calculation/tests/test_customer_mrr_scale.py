# TODO
# import datetime
#
# from odoo.tests.common import TransactionCase
#
#
# class TestCustomerMrrScale(TransactionCase):
#     def with_context(self, *args, **kwargs):
#         context = dict(args[0] if args else self.env.context, **kwargs)
#         self.env = self.env(context=context)
#         return self
#
#     def setUp(self):
#         super().setUp()
#
#         self.chart = self.env["account.chart.template"].search([], limit=1)
#
#         self.company = self.env["res.company"].create(
#             {
#                 "name": "Test company",
#             }
#         )
#         self.env.ref("base.group_multi_company").write(
#             {
#                 "users": [(4, self.env.uid)],
#             }
#         )
#         self.env.user.write(
#             {
#                 "company_ids": [(4, self.company.id)],
#                 "company_id": self.company.id,
#             }
#         )
#         self.with_context(company_id=self.company.id, force_company=self.company.id)
#         self.chart.try_loading_for_current_company()
#
#         # Criar registros necessários para o teste
#         self.res_partner_obj = self.env["res.partner"]
#         self.weni_customer_mrr_scale_obj = self.env["weni.customer.mrr.scale"]
#         self.account_invoice_obj = self.env["account.invoice"]
#         self.account_invoice_line_obj = self.env["account.invoice.line"]
#
#         self.account_receivable = self.env["account.account"].search(
#             [
#                 (
#                     "user_type_id",
#                     "=",
#                     self.env.ref("account.data_account_type_receivable").id,
#                 )
#             ],
#             limit=1,
#         )
#         self.account_revenue = self.env["account.account"].search(
#             [
#                 (
#                     "user_type_id",
#                     "=",
#                     self.env.ref("account.data_account_type_revenue").id,
#                 )
#             ],
#             limit=1,
#         )
#
#         self.journalrec = self.env["account.journal"].search(
#             [("type", "=", "sale")], limit=1
#         )
#
#         self.scale_1 = self.weni_customer_mrr_scale_obj.create(
#             {
#                 "min_value": 0,
#                 "max_value": 1000,
#             }
#         )
#
#         self.scale_2 = self.weni_customer_mrr_scale_obj.create(
#             {
#                 "min_value": 1001,
#                 "max_value": 2000,
#             }
#         )
#
#         self.partner_1 = self.res_partner_obj.create(
#             {
#                 "name": "Partner 1",
#                 "is_company": True,
#             }
#         )
#
#         self.partner_2 = self.res_partner_obj.create(
#             {
#                 "name": "Partner 2",
#                 "is_company": True,
#             }
#         )
#
#         self.invoice_1 = self.account_invoice_obj.create(
#             {
#                 "partner_id": self.partner_1.id,
#                 "date_invoice": datetime.date.today() - datetime.timedelta(days=10),
#                 "type": "out_invoice",
#                 "journal_id": self.journalrec.id,
#                 "account_id": self.account_receivable.id,
#             }
#         )
#
#         self.invoice_line_1 = self.account_invoice_line_obj.create(
#             {
#                 "invoice_id": self.invoice_1.id,
#                 "name": "Invoice Line 1",
#                 "price_unit": 500,
#                 "quantity": 1,
#                 "account_id": self.account_revenue.id,
#             }
#         )
#
#         self.invoice_2 = self.account_invoice_obj.create(
#             {
#                 "partner_id": self.partner_2.id,
#                 "date_invoice": datetime.date.today() - datetime.timedelta(days=15),
#                 "type": "out_invoice",
#                 "journal_id": self.journalrec.id,
#                 "account_id": self.account_receivable.id,
#             }
#         )
#
#         self.invoice_line_2 = self.account_invoice_line_obj.create(
#             {
#                 "invoice_id": self.invoice_2.id,
#                 "name": "Invoice Line 2",
#                 "price_unit": 1500,
#                 "quantity": 1,
#                 "account_id": self.account_revenue.id,
#             }
#         )
#
#         self.invoice_1.action_invoice_open()
#         self.invoice_2.action_invoice_open()
#
#     def test_compute_mrr(self):
#         # Testando a função _compute_mrr com um valor dentro da escala_1
#         result_1 = self.res_partner_obj._compute_mrr(500)
#         self.assertEqual(
#             result_1, self.scale_1, "A escala MRR calculada está incorreta."
#         )
#
#         # Testando a função _compute_mrr com um valor dentro da escala_2
#         result_2 = self.res_partner_obj._compute_mrr(1500)
#         self.assertEqual(
#             result_2, self.scale_2, "A escala MRR calculada está incorreta."
#         )
#
#     def test_cron_update_mrr(self):
#         # Executando a função _cron_update_mrr
#         self.res_partner_obj._cron_update_mrr()
#
#         # Verificar se a escala MRR foi atualizada corretamente
#         self.assertEqual(
#             self.partner_1.weni_customer_mrr_scale_id,
#             self.scale_1,
#             "A escala MRR não foi atualizada corretamente.",
#         )
#         self.assertEqual(
#             self.partner_2.weni_customer_mrr_scale_id,
#             self.scale_2,
#             "A escala MRR não foi atualizada corretamente.",
#         )
