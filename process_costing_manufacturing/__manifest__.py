{
    'name': 'Manufacturing Costing',
    'version': '15.1',
    'category': 'Manufacturing',
    'author': 'Asem tal3t',
    'category': 'Manufacturing',
    'depends': ['sale_management','mrp','mrp_account_enterprise','account'],
    'data': [
            'security/ir.model.access.csv',
            'views/custom_bom_view.xml',
            'report/mrp_costing_report.xml',
            'report/mrp_bom_report_view.xml',
            'report/mrp_production_report_view.xml',
            'report/cost_analysis.xml',
    ],
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
}

