# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel

class ResPartnerNpsInput(Datamodel):
    _name = "res.partner.nps.input"

    id = fields.Integer(required=True, allow_none=False)

''
class ResPartnerNpsOutput(Datamodel):
    _name = "res.partner.nps.output"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    nps = fields.Integer(required=True, allow_none=False)
    channel_id = NestedModel('weni.partner.nps.channel', required=True, allow_none=False, many=True)
    partner_id = NestedModel('res.partner', required=True, allow_none=False, many=True)
    contact_id = NestedModel('res.partner', required=True, allow_none=False, many=True)