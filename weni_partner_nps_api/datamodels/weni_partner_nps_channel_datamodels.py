from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel
from odoo.addons.datamodel import fields


class WeniPartnerNpsChannelInput(Datamodel):
    _name = "weni.partner.nps.channel.input"

    id = fields.Integer(required=True, allow_none=False)


class WeniPartnerNpsChannelOutput(Datamodel):
    _name = "weni.partner.nps.channel.output"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)


class WeniPartnerNpsChannelSearchInput(Datamodel):
    _name = "weni.partner.nps.channel.search.input"

    id = fields.Integer(required=False, allow_none=False)


class WeniPartnerNpsChannelSearchOutput(Datamodel):
    _name = "weni.partner.nps.channel.search.output"

    size = fields.Integer(required=False, allow_none=False)
    data = NestedModel(
        "weni.partner.nps.channel.output",
        required=False,
        allow_none=True,
        many=True,
    )