# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResPartnerNps(TransactionCase):
    def setUp(self):
        super().setUp()

        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )

        self.contact = self.env["res.partner"].create(
            {
                "name": "Test Contact",
            }
        )

        self.channel = self.env["weni.partner.nps.channel"].create(
            {
                "name": "Test Channel",
            }
        )

    def test_res_partner_nps_create(self):
        nps_record = self.env["res.partner.nps"].create(
            {
                "submission_date": "2023-04-17",
                "partner_id": self.partner.id,
                "contact_id": self.contact.id,
                "channel_id": self.channel.id,
                "nps": 7,
                "comment": "Test comment",
            }
        )

        self.assertEqual(nps_record.partner_id, self.partner)
        self.assertEqual(nps_record.contact_id, self.contact)
        self.assertEqual(nps_record.channel_id, self.channel)
        self.assertEqual(nps_record.nps, 7)
        self.assertEqual(nps_record.comment, "Test comment")

    def test_res_partner_nps_compute_name(self):
        nps_record = self.env["res.partner.nps"].create(
            {
                "submission_date": "2023-04-17",
                "partner_id": self.partner.id,
                "contact_id": self.contact.id,
                "channel_id": self.channel.id,
                "nps": 7,
                "comment": "Test comment",
            }
        )

        nps_record._compute_name()

        expected_name = "2023-04-17 / Test Partner / Test Contact"
        self.assertEqual(nps_record.name, expected_name)
