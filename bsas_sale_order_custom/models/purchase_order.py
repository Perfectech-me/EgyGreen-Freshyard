from odoo import models, fields, api
class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    order_category = fields.Selection(string="Order Catrgory", selection=[
        ('International', 'International'),
        ('Local', 'Local'),
        ('Export', 'Export'),
    ], default='International')

    export_type = fields.Selection(string="Export Type", selection=[('fresh', 'fresh'), ('frozen', 'frozen'),
                                                                    ('food_products', 'Food Products'), ],
                                   default='fresh')
    product_type = fields.Selection(string="Product Type", selection=[
        ('row_materials', 'Row Materials'), ('sort', 'Sort'), ('packing', 'Packing'),
        ('finish_products', 'Finish Products'), ('other', 'Other')], default='row_materials')



