# Copyright 2022 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Weni Partner Nps',
    'summary': """
        WENI Partner NPS""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo',
    'website': 'https://github.com/escodoo/weni-addons',
    'depends': [
        'contacts',
        'sales_team',
    ],
    'data': [
        'security/weni_partner_nps_channel.xml',
        'views/weni_partner_nps_channel.xml',
        # 'data/res_partner_category.xml',
        'data/weni_partner_nps_cron.xml',
        'security/res_partner_nps.xml',
        'views/res_partner_nps.xml',
        'views/res_partner.xml',
    ],
    'demo': [
    ],
}
