# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re
from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):
        aliases = self.env["mail.alias"].search([("weni_mail_blacklist_ids", "!=", False)])
        if aliases:
            matching_aliases = self._find_matching_aliases(message_dict)
            if matching_aliases:
                recipients = ",".join(
                    [message_dict["recipients"]]
                    + matching_aliases.mapped("display_name")
                )
                message_dict["recipients"] = recipients
            if not self._contains_blacklist_emails(message_dict.get("from", "")):
                return False
        else:
            pass

        return super().message_route(
            message, message_dict, model, thread_id, custom_values
        )

    def _find_matching_aliases(self, message_dict):
        pass
    
    def _contains_blacklist_emails(self, sender_email):
        if sender_email:
            # Get email in characters < >, default response is FirstName LastName <name@email.com>
            sender_email = re.search(r'<([^>]+)>', sender_email).group(1)
            # Search all mails blacklist
            aliases = self.env["mail.alias"].search([("weni_mail_blacklist_ids", "!=", False)])
            for alias in aliases:
                blacklist_emails = alias.weni_mail_blacklist_ids.mapped('weni_blacklist_mail')
                if sender_email in blacklist_emails:
                    # Return False to stop process alias, example: create helpdesk.ticket
                    return False
        # Allow continue process to alias
        return True
