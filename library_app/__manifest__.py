{
    "name": "Library Management",
    "summary": "Manage library catalog and book lending.",
    "author": "Tris",
    "license": "AGPL-3",
    "depends": ["base"],
    "application": True,
    "category": "Services/Library",
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/library_menu.xml",
        "views/book_view.xml",
        "views/book_list_template.xml",
        "reports/library_book_report.xml",
        "reports/library_publisher_report.xml"
    ],

    "demo": [
        "demo/res.partner.csv",
        "demo/library.book.csv",
        "demo/book_demo.xml"
    ]
}
