# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProjectTaskKanbanState(TransactionCase):
    def setUp(self):
        super().setUp()
        self.weni_state = self.env["project.task.kanban.state"].create(
            {"name": "Teste", "color": "#F65643"}
        )

    def test_search_records_by_name(self):
        result = self.weni_state.search_records_by_name("Teste")
        expected_result = [{"name": "Teste", "color": "#F65643"}]
        self.assertEqual(result, expected_result)
