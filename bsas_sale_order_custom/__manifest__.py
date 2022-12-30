# -*- coding: utf-8 -*-
{
    'name': "Sale Order Customize",
    'category': 'Sales',
    'version': '15.0',
    'depends': ['base','sale','sale_management','bi_customer_limit','bsas_additional_cost','purchase','sale_stock','stock_account'],

    'data': [
        'security/access_group.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/sale_order.xml',
        'views/port_loading.xml',
        'views/purchase_order.xml',
        'views/shipment_line.xml',
        'views/sales_person_users.xml',
        'views/account_move.xml',
        'views/container_type.xml',
        'views/stock_valuation._ayer.xml',
        'wizard/approve_credit_limit.xml',
        'wizard/refuse_credit_limit.xml',
    ],
    'license': 'LGPL-3',

}
