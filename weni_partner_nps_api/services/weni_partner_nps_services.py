# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest import restapi
from odoo.addons.datamodel.core import Datamodel
from odoo.addons.component.core import Component


class WeniPartnerNpsService(Component):
    _inherit = "base.weni.rest.service"
    _name = "weni.res.partner.nps.service"
    _usage = "partner_nps"
    _expose_model = "res.partner.nps"
    _description = """
    Res Partner Nps Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("res.partner.nps.output"),
    )
    def get(self, _id):
        record = self._get(_id)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/search"], "GET")],
        input_param=Datamodel("res.partner.nps.input"),
        output_param=Datamodel("res.partner.nps.output"),
    )
    def search(self, filters):
        domain = self._get_base_search_domain(filters)
        records = self.env[self._expose_model].search(domain)
        result = {"size": len(records), "data": self._to_json(records, many=True)}
        return self.env.datamodels["res.partner.nps.output"].load(result)

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=restapi.Datamodel("res.partner.nps.input"),
        output_param=restapi.Datamodel("res.partner.nps.output"),
    )
    # pylint: disable=W8106
    def create(self, record):
        vals = self._prepare_params(record.dump())
        record = self.env[self._expose_model].create(vals)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("res.partner.nps.input"),
    )
    def update(self, values):
        record = self._get(values.id)
        record.write(self._prepare_params(values.dump()))
        return self._to_json(record)

    @restapi.method(
        routes=[(["/delete/<int:id>"], "DELETE")],
    )
    def delete(self, _id):
        record = self._get(_id)
        if record.exists():
            record.unlink()
            return {"response": "Record deleted"}
        else:
            return {"response": "No record found"}

    def _prepare_params(self, params):
        for key in [
            "id",
            "name",
            "nps",
        ]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    def _json_parser(self):
        res = [
            "id",
            "name",
            "nps"
            ("channel_id:channel", ["id", "name"]),
            ("contact_id:contact", ["id", "name"]),
            ("partner_id:partner", ["id", "name"]),
        ]
        return res

    def _get_base_search_domain(self, filters):
        domain = super()._get_base_search_domain(filters)
        # res += [("partner_id", "=", self.env.context.get("authenticated_partner_id"))]
        if filters:
            if filters.id:
                domain += [("id", "=", filters.id)]
            if filters.name:
                domain.append(("name", "like", filters.name))
            if filters.nps:
                domain.append(("nps", "like", filters.name))
            if filters.channel_id:
                domain.append(("channel_id", "like", filters.name))
            if filters.contact_id:
                domain.append(("contact_id", "like", filters.name))
            if filters.partner_id:
                domain.append(("partner_id", "like", filters.name))
        return domain