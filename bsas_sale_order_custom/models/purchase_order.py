from odoo import models, fields, api

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    analytic_tag_ids = fields.Many2many('account.analytic.tag',compute = '_set_analytic_tag_ids',store = True)
    analytic_account_ids = fields.Many2many('account.analytic.account',compute = '_set_analytic_tag_ids',store = True)
    @api.depends('order_line.analytic_tag_ids','order_line.account_analytic_id',)
    def _set_analytic_tag_ids(self):
        for rec in self:
            ids = []
            ids_2 = []
            for line in rec.order_line:
                ids += line.analytic_tag_ids.ids
                ids_2 += line.account_analytic_id.ids
                
            rec.analytic_tag_ids = [(6,0,ids)]
            rec.analytic_account_ids = [(6,0,ids_2)]
    order_category = fields.Selection(string="Order Catrgory", selection=[
        ('International', 'International'),
        ('Local', 'Local'),
    ], default='International')

    export_type = fields.Selection(string="Type", selection=[('fresh', 'fresh'), ('frozen', 'frozen'),
                                                                    ('food_products', 'Food Products'),
                                                                    ('service', 'Service'),
                                                                    ('other', 'Other'),
                                                             ],
                                   default='fresh')
    product_type = fields.Selection(string="Product Type", selection=[
        ('row_materials', 'Row Materials'), ('sort', 'Sort'), ('packing', 'Packing'),
        ('finish_products', 'Finish Products'), ('other', 'Other')], default='row_materials')



