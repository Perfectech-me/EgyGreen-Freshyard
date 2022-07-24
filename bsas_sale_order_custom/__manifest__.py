# -*- coding: utf-8 -*-
{
    'name': "Sale Order Customize",
    'category': 'Sales',
    'version': '15.0',
    'depends': ['base','sale','sale_management','bi_customer_limit','bsas_additional_cost'],

    'data': [
        'security/ir.model.access.csv',
        'security/access_group.xml',
        'data/data.xml',
        'views/sale_order.xml',
        'views/port_loading.xml',
        'wizard/approve_credit_limit.xml',
    ],
    'license': 'LGPL-3',

}
