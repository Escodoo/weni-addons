from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel

class WeniPartnerNpsChannelInput(Datamodel):
    _name = "weni.partner.nps.channel.input"

    id = fields.Integer(required=True, allow_none=False)


class WeniPartnerNpsChannelOutput(Datamodel):
    _name = "weni.partner.nps.channel.output"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)