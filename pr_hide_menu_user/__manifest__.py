# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybernetics Plus Co., Ltd.
#    Hide Menu for User
#
###################################################################################

{
    'name': 'Hide Menu for User',
    'version': '15.0.1.0.1',
    'summary': """ 
            Cybernetics Plus Tools Hide Menu for User
            .""",
    'description': """ 
            Cybernetics Plus Tools Hide Menu for User
            .""",
    'author': 'Cybernetics Plus Co., Ltd.',
    'company': 'Cybernetics Plus Co., Ltd.',
    'maintainer': 'Cybernetics Plus Co., Ltd.',
    'website': 'https://www.cybernetics.plus',
    'live_test_url': 'https://www.cybernetics.plus',
    'images': ['static/description/banner.png'],
    'category': 'Tools',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'contributors': [
        'Developer <dev@cybernetics.plus>',
    ],
    'depends': ['base'],
    'data': [
        'views/res_users.xml',
        'views/res_security.xml'
    ],
}
