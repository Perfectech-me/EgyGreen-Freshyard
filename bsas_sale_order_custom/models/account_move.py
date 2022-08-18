from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    invoice_person_user_id = fields.Many2one(comodel_name="sales.person.users", string="Sales Person")
    bank_ids = fields.Many2many(comodel_name="res.partner.bank",string="Bank Accounts")
    sales_order_id = fields.Many2one(comodel_name="sale.order")
    not_local_sale_order = fields.Boolean(compute='_get_check_not_local_sale_order')

    @api.depends('sales_order_id')
    def _get_check_not_local_sale_order(self):
        for rec in self:
            if rec.sales_order_id and rec.sales_order_id.order_category!='Local':
                rec.not_local_sale_order = True
            else:
                rec.not_local_sale_order = False


