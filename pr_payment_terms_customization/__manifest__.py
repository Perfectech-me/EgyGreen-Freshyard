# -*- coding: utf-8 -*-
{
    'name': 'Payment Terms Customization',
    'version': '15',
    'summary': 'Payment Terms Customization',
    'author': 'Perfect-tech - Mohamed Salem',
    'license': 'LGPL-3',
    'depends': ['sale', 'account', 'base', 'product', 'analytic'],
    'data': [
        'views/payment_terms_view.xml',
        'views/inherited_account_move.xml',
    ],
    'installable': True,
    'auto_install': False,
}
