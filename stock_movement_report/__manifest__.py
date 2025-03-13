# -*- coding: utf-8 -*-
{
    'name': "Stock Movement Report",
    'summary': "Generate detailed reports of stock movements per product or location.",
    'description': """
       Generate detailed reports of stock movements per product or location.
    """,

    'author': "PerfectTech",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'views/stock_move_line_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
