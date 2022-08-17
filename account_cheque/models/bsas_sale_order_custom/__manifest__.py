# -*- coding: utf-8 -*-
{
    'name': "Sale Order Customize",
    'category': 'Sales',
    'version': '15.0',
    'depends': ['base','sale','sale_management','bi_customer_limit','bsas_additional_cost','purchase','sale_stock'],

    'data': [
        'security/ir.model.access.csv',
        'security/access_group.xml',
        'data/data.xml',
        'views/sale_order.xml',
        'views/port_loading.xml',
        'views/purchase_order.xml',
        'views/shipment_line.xml',
        'views/sales_person_users.xml',
        'views/account_move.xml',
        'views/res_partner.xml',
        'views/customer_type.xml',
        'wizard/approve_credit_limit.xml',
        'wizard/refuse_credit_limit.xml',
    ],
    'license': 'LGPL-3',

}