# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email.message import Message

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestMailThread(TransactionCase):
    def setUp(self):
        super().setUp()
        self.MailAlias = self.env["mail.alias"]
        self.MailThread = self.env["mail.thread"]
        self.user_group = self.env.ref("base.group_user")

    def test_message_route_with_whitelist_words(self):
        alias = self.MailAlias.create(
            {
                "alias_name": "support@example.com",
                "alias_model_id": self.env["ir.model"]._get("res.partner").id,
                "whitelist_words": "urgent,help",
            }
        )
        self.assertTrue(alias)
        message_dict = {
            "recipients": "support@example.com",
            "body": "This is an urgent request. Please help.",
        }
        # Create a simple email message object
        message = Message()
        message["Subject"] = "Test email"
        message.set_payload("This is a test email.")
        result = self.MailThread.message_route(
            message=message,
            message_dict=message_dict,
            model=self.env["ir.model"]._get("res.partner").model,
            thread_id=None,
            custom_values=None,
        )
        self.assertTrue(result, "The message_route should not return False.")
        self.assertIn(
            "support@example.com",
            message_dict["recipients"],
            "The recipients should include the mail alias.",
        )

    def test_message_route_without_matching_whitelist_words(self):
        alias = self.MailAlias.create(
            {
                "alias_name": "support@example.com",
                "alias_model_id": self.env["ir.model"]._get("res.partner").id,
                "whitelist_words": "urgent,help",
            }
        )
        self.assertTrue(alias)
        message_dict = {
            "recipients": "support@example.com",
            "body": "This is a general inquiry.",
        }
        message = Message()
        message["Subject"] = "Test email"
        message.set_payload("This is a test email.")
        result = self.MailThread.message_route(
            message=message,
            message_dict=message_dict,
            model=self.env["ir.model"]._get("res.partner").model,
            thread_id=None,
            custom_values=None,
        )
        self.assertFalse(result, "The message_route should return False.")
