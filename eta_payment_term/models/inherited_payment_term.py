# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class eta_payment_term(models.Model):
#     _name = 'eta_payment_term.eta_payment_term'
#     _description = 'eta_payment_term.eta_payment_term'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
