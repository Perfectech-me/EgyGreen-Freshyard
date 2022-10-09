# -*- coding: utf-8 -*-
from odoo import http

# class AccountCheque(http.Controller):
#     @http.route('/account_cheque/account_cheque/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_cheque/account_cheque/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_cheque.listing', {
#             'root': '/account_cheque/account_cheque',
#             'objects': http.request.env['account_cheque.account_cheque'].search([]),
#         })

#     @http.route('/account_cheque/account_cheque/objects/<model("account_cheque.account_cheque"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_cheque.object', {
#             'object': obj
#         })