# -*- coding: utf-8 -*-
{
    'name': "Sale Order Customize",
    'category': 'Sales',
    'version': '15.0',
    'depends': ['base','sale','sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/sale_order.xml',
        'views/port_loading.xml',
    ],
    'license': 'LGPL-3',

}
