# -*- coding: utf-8 -*-
{
    'name': "Product Additional Cost",
    'author': "Mohamed Salah",
    'category': 'Sales',
    'version': '15',
    'depends': ['base','sale','sale_management','purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/product.xml',
        'views/partner.xml',
        'wizard/product_cost_wizard.xml',
    ],
    'license': 'LGPL-3',

}
