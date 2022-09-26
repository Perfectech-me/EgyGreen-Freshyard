# -*- coding: utf-8 -*-
{
    'name': "Account Partner Ledger Report",

    'description': """
        Custom Account Partner Ledger Report
    """,

    'author': "Mohamed Salah",
    'category': 'Accounting Reports',
    'version': '15',

    'depends': ['base','account_accountant','account_reports','web'],

    # always loaded
    'data': [
            'views/search_template_view.xml',

    ],
    'license': 'LGPL-3',

    'assets': {
        'web.assets_backend': [
            'account_partner_ledger_report/static/src/js/custom_account_reports.js'
        ],
    }

}
