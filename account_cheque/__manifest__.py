# -*- coding: utf-8 -*-
{
    'name': "Accounting checks",

    'description': """
        Accounting Checks
    """,
    'category': 'Accounting',
    'version': '15.1',
    'depends': ['base', 'account'],
    'data': [
        'security/cheque_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/cashed_outgoing_wizard.xml',
        'reports/incoming_report.xml',
        'reports/outgoing_report.xml',
        'reports/print_cheque.xml',
        'reports/cheque_print.xml',
        'reports/epe_check.xml',
        'reports/cib_cheque.xml',
        'reports/wafa_cheque.xml',
    ],

    'license': 'LGPL-3',
}
