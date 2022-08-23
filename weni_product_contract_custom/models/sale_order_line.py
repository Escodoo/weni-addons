# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    def _get_date_end(self):
        # Originally the suggested end date is multiplied by the number
        # of items. In this case we are multiplying by 12.

        self.ensure_one()

        # It is necessary to completely overwrite this method because when
        # selling a large amount of the product, the system returns an error
        # when calculating the original end date since there was an overflow
        # of the allowed range of years.
        # super()._get_date_end()

        contract_line_model = self.env["contract.line"]
        date_end = (
            self.date_start
            + contract_line_model.get_relative_delta(
                self._get_auto_renew_rule_type(),
                12,
            )
            - relativedelta(days=1)
        )
        return date_end

    def _get_contract_line_qty(self):
        # Originally the return value is 1 but in this case we override t
        # he method to use the amount of the sales order.

        self.ensure_one()
        super()._get_contract_line_qty()
        return self.product_uom_qty
