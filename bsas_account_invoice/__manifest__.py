# -*- coding: utf-8 -*-
{
    'name': "Bsas Account Invoice",

    'category': 'Accounting',
    'version': '15.0',
    'depends': ['base','account','account_accountant'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move.xml',
        'report/invoice_report.xml',
    ],
    'license': 'LGPL-3',

}
