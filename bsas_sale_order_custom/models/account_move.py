from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    invoice_person_user_id = fields.Many2one(comodel_name="sales.person.users", string="Sales Person")
    bank_ids = fields.Many2many(comodel_name="res.partner.bank",string="Bank Accounts")
    sales_order_id = fields.Many2one(comodel_name="sale.order")
    not_local_sale_order = fields.Boolean(compute='_get_check_not_local_sale_order')
    supplier_invoice = fields.Char(string="Supplier Invoice")

    @api.depends('sales_order_id')
    def _get_check_not_local_sale_order(self):
        for rec in self:
            if rec.sales_order_id and rec.sales_order_id.order_category!='Local':
                rec.not_local_sale_order = True
            else:
                rec.not_local_sale_order = False


class AccountAnalyticTagInherit(models.Model):
    _inherit = 'account.analytic.tag'

    _sql_constraints = [
        ('tag_unique', 'UNIQUE (name)', 'Analytic Tag Must Be Unique')
    ]


class StockValuationLayerInherit(models.Model):
    _inherit = 'stock.valuation.layer'

    categ_id = fields.Many2one('product.category', compute='product_id.categ_id',)
    product_category_name = fields.Char(string="Category")

    @api.model
    def create(self, vals):
        res = super(StockValuationLayerInherit, self).create(vals)
        if res.product_id:
            res.product_category_name=res.product_id.categ_id.name
        return res

    # def _inverse_partner_data(self):
    #     for rec in self:
    #         rec.product_category_id=rec.product_id.categ_id.id
    #
    # @api.depends('product_id')
    # def product_category(self):
    #     for rec in self:
    #         rec.product_category_id=False
    #         if rec.product_id:
    #             rec.product_category_id = rec.product_id.categ_id.id