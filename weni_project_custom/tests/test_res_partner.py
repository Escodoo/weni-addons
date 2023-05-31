# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartner(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("base.res_partner_1")
        self.project = self.env["project.project"].create(
            {
                "name": "Project X",
                "partner_id": self.partner.id,
            }
        )
        self.project2 = self.env["project.project"].create(
            {
                "name": "Project Y",
                "partner_id": self.partner.id,
            }
        )
        self.project3 = self.env["project.project"].create(
            {
                "name": "Project Z",
                "partner_id": self.partner.id,
            }
        )

    def test_compute_project_count(self):
        self.partner._compute_project_count()
        self.assertEqual(
            self.partner.project_count, 3, "Partner should have 3 projects"
        )
