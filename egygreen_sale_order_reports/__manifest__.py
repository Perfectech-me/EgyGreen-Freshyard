# -*- coding: utf-8 -*-
{
    'name': "Sale Order Reports",
    'description': """
            Sale Order Custom Reports
        """,

    'author': "Mohamed Salah",
    'category': 'Sales',
    'version': '15.0',
    'depends': ['base','sale'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_view.xml',
        'reports/sale_report.xml',
        'reports/invoice_preforma_report.xml',
        'reports/shipping_order_warehouse.xml',
    ],

}
