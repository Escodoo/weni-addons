# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductProduct(models.Model):

    _inherit = 'product.product'

    # surplus_product_id = fields.Many2one(
    #     'product.product',
    #     string='Surplus Product',
    # )
