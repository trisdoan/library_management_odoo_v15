# -*- coding: utf-8 -*-
{
    'name': "Library Website Portal",


    'description': """
        Portal for library members
    """,

    'author': "Tris",
    # any module necessary for this one to work correctly
    'depends': ['library_checkout', 'portal'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "security/library_security.xml",
        "views/main_templates.xml",
        "views/portal_templates.xml",
    ],
    "assets": {
        "web.assets_backend": {
            "library_portal/static/src/css/library.css",
        }
    }
}
