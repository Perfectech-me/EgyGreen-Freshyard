# -*- coding: utf-8 -*-
{
    'name': "Sale Order Reports",
    'description': """
            Sale Order Custom Reports
        """,

    'author': "Mohamed Salah",
    'category': 'Sales',
    'version': '15.0',
    'depends': ['base','sale','account','bsas_sale_order_custom','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/account_move.xml',
        'views/company.xml',
        'reports/sale_report.xml',
        'reports/invoice_preforma_report.xml',
        'reports/shipping_order_warehouse.xml',
        'reports/marine_insurance.xml',
        'reports/final_invoice_clearance.xml',
        'reports/final_invoice_lc.xml',
        'reports/sale_wizard_reports.xml',
        'wizard/sale_wizard_report.xml',
    ],

}
