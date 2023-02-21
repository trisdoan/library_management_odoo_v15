# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Real Estate",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
        "data/data.xml",
        "report/report_property_offers.xml",
        "report/report_property_view.xml"
    ],
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
    "license": "LGPL-3",
    "category": "Real Estate/Brokerage",
}
