# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


# from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel
from odoo.addons.datamodel import fields


class ResPartnerNpsInput(Datamodel):
    _name = "res.partner.nps.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)


class ResPartnerNpsOutput(Datamodel):
    _name = "res.partner.nps.output"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    nps = fields.Integer(required=False, allow_none=False)
    channel = NestedModel('weni.partner.nps.channel.output', required=False, allow_none=True)
    partner = NestedModel('res.partner.output', required=False, allow_none=False)
    contact = NestedModel('res.partner.output', required=False, allow_none=False)


class ResPartnerNpsSearchInput(Datamodel):
    _name = "res.partner.nps.search.input"

    id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    nps = fields.Integer(required=False, allow_none=True)


class ResPartnerNpsSearchOutput(Datamodel):
    _name = "res.partner.nps.search.output"

    size = fields.Integer(required=False, allow_none=False)
    data = NestedModel(
        "res.partner.nps.output",
        required=False,
        allow_none=True,
        many=True,
    )

