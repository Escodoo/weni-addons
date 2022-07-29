# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel
from odoo.addons.datamodel import fields


class ResPartnerInput(Datamodel):
    _name = "res.partner.input"

    id = fields.Integer(required=False, allow_none=False)
    weni_id = fields.String(required=False, allow_none=False)


class ResPartnerOutput(Datamodel):
    _name = "res.partner.output"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    weni_id = fields.String(required=False, allow_none=True)
    weni_nps_count = fields.Integer(required=False, allow_none=False)
    weni_current_nps = fields.Integer(required=False, allow_none=False)
    # weni_nps_ids = NestedModel('res.partner.nps.output', required=False, allow_none=False)


class ResPartnerSearchInput(Datamodel):
    _name = "res.partner.search.input"

    id = fields.Integer(required=False, allow_none=False)
    weni_id = fields.String(required=False, allow_none=False)


class ResPartnerSearchOutput(Datamodel):
    _name = "res.partner.search.output"

    size = fields.Integer(required=False, allow_none=False)
    data = NestedModel(
        "res.partner.output",
        required=False,
        allow_none=True,
        many=True,
    )