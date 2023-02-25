# -*- coding: utf-8 -*-

{"name": "Library Book Checkout",
 'description': "Members can borrow books from the library.",
 "author": "Tris",
 "license": "LGPL-3",
 "depends": ["library_member", 'mail', 'contacts'],
 "data": [
     "security/ir.model.access.csv",
     "wizard/checkout_mass_message_wizard_view.xml",
     "views/library_menu.xml",
     "views/checkout_view.xml",
     "views/checkout_kanban_view.xml",
     "data/library_checkout_stage.xml",
 ],
 "assets": {
     "web.assets_backend": {
         "library_checkout/static/src/css/checkout.css",
         "library_checkout/static/src/js/checkout.js",
         }
     }
 }
