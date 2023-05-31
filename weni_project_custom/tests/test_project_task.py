# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProjectTask(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("base.res_partner_1")
        self.project = self.env["project.project"].create(
            {
                "name": "Project X",
                "partner_id": self.partner.id,
            }
        )
        self.task = self.env["project.task"].create(
            {
                "name": "Task",
                "priority": "0",
                "kanban_state": "normal",
                "project_id": self.project.id,
                "partner_id": self.partner.id,
            }
        )
        self.weni_kanban_state = self.env["project.task.kanban.state"].create(
            {"name": "Teste", "color": "#F65643"}
        )

    def test_compute_kanban_state_label(self):
        self.task._compute_kanban_state_label()
        self.assertEqual(self.task.kanban_state, "normal")

        self.task.kanban_state = "blocked"
        self.task._compute_kanban_state_label()
        self.assertEqual(self.task.kanban_state, "blocked")

        self.task.kanban_state = self.weni_kanban_state.name
        self.task._compute_kanban_state_label()
        weni_states = self.env["project.task.kanban.state"].search(
            [("name", "=", self.task.kanban_state)]
        )
        self.assertTrue(weni_states)
        expected_label = weni_states.name
        self.assertEqual(self.task.kanban_state_label, expected_label)

        self.task.kanban_state_label = self.task.legend_done
        expected_label = self.task.legend_done
        self.assertEqual(self.task.kanban_state_label, expected_label)
