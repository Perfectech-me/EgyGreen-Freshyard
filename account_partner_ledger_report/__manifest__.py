# -*- coding: utf-8 -*-
{
    'name': "Account Partner Ledger Report",

    'description': """
        Custom Account Partner Ledger Report
    """,

    'author': "Mohamed Salah",
    'category': 'Accounting Reports',
    'version': '15',

    'depends': ['base','account_accountant','account_reports','web','report_xlsx'],

    # always loaded
    'data': [
            'security/ir.model.access.csv',
            'views/search_template_view.xml',
            'wizard/partner_ledger_custom_report.xml',
            'reports/partner_ledger_report.xml',

    ],
    'license': 'LGPL-3',

    'assets': {
        'web.assets_backend': [
            'account_partner_ledger_report/static/src/js/custom_account_reports.js'
        ],
    }

}
