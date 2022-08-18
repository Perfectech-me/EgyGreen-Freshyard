from odoo import models, fields, api

class AccountTaxInherit(models.Model):
    _inherit = 'account.tax'

    without_holding = fields.Boolean(string="Without Holding")
