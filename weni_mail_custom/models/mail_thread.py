# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):
        aliases = self.env["mail.alias"].search([("whitelist_words", "!=", "")])
        if aliases:
            matching_aliases = self._find_matching_aliases(message_dict)
            if matching_aliases:
                recipients = ",".join(
                    [message_dict["recipients"]]
                    + matching_aliases.mapped("display_name")
                )
                message_dict["recipients"] = recipients
            if not self._contains_whitelist_words(message_dict.get("body", "")):
                return False
        else:
            pass

        return super().message_route(
            message, message_dict, model, thread_id, custom_values
        )

    def _find_matching_aliases(self, message_dict):
        pass

    def _contains_whitelist_words(self, body):
        if body:
            body = body.lower()
            aliases = self.env["mail.alias"].search([("whitelist_words", "!=", "")])
            for alias in aliases:
                whitelist_words = [
                    word.strip().lower() for word in alias.whitelist_words.split(",")
                ]
                for word in whitelist_words:
                    if word in body:
                        return True
        return False
