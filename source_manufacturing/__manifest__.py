# -*- coding: utf-8 -*-
{
    'name': "Source Manufacturing",
    'summary': "Source Manufacturing",
    'description': """
      Source Manufacturing.
    """,
    'author': "PerfectTech",
    'website': "http://www.yourcompany.com",
    'version': '0.1',
    'depends': ['base', 'mrp','stock','account'],
    'data': [
        'views/mrp_production_views.xml',
        'views/stock_move_line_views.xml'
    ],

}
