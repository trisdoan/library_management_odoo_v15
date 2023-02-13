# -*- coding: utf-8 -*-
{
    'name': "library_member",

    'description': """
        Manage members borrowing books.
    """,
    "author": "Tris Doan",
    "license": "AGPL-3",
    "depends": ["library_app", "mail"],
    "application": False,
    "data": [
        "security/ir.model.access.csv",
        "views/book_view.xml",
        "views/member_view.xml",
        "views/library_menu.xml",
        "views/book_list_template.xml"
    ]
}
