from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    invoice_person_user_id = fields.Many2one(comodel_name="sales.person.users", string="Sales Person")
    bank_ids = fields.Many2many(comodel_name="res.partner.bank",string="Bank Accounts")


