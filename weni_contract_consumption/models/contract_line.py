# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    contract_line_consumption_ids = fields.One2many(
        "contract.line.consumption", "contract_line_id", "Contract Consumption"
    )
