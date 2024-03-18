{
    "name": "Real Estate Ads",
    "version": "1.0",
    "author": "Bereza Damian",
    "description": """
        Real Estate module to show abailable properties
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/menu_items.xml',

    ],
    "license": "LGPL-3",

}