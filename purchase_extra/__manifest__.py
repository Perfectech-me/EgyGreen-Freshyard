{
    'name': "purchase extra",

    'summary': """ """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','purchase'],

    # always loaded
    'data': [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/purchase_extra.xml',

    ],

    'license': 'OEEL-1',
    # 'installable': True,
}
# -*- coding: utf-8 -*-
