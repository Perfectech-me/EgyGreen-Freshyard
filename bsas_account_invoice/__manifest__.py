# -*- coding: utf-8 -*-
{
    'name': "Bsas Account Invoice",

    'category': 'Accounting',
    'version': '15.0',
    'depends': ['base','account','account_accountant','purchase_extra','bsas_sale_order_custom'],
    'data': [
        'views/account_move.xml',
        'views/partner.xml',
        'views/taxes.xml',
        'report/invoice_report.xml',
        'report/receipt_discount_tax_report.xml',
    ],
    'license': 'LGPL-3',

}
