from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    data_loger = fields.Text(string="Data Loger")

