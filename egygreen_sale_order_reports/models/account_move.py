from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        result = super(AccountMoveInherit, self).create(vals)
        result.partner_bank_id=result.sale_order_id.partner_bank_id.id
        return result