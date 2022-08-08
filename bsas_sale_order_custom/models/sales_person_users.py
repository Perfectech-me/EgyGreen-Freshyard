from odoo import models, fields, api
class SalesPersonUsers(models.Model):
    _name = 'sales.person.users'
    _rec_name = 'name'
    _description = 'Sales Person Users'

    name = fields.Char()

