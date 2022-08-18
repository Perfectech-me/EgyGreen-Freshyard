from odoo import models, fields, api

class ProductAdditionalCost(models.TransientModel):
    _name = 'product.additional.cost'

    product_ids = fields.Many2many(comodel_name="product.product")

    def button_add_product_additional_cost(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids'))
        if sale_order:
            lines=[]
            for line in self.product_ids:
                lines.append((0, 0, {
                    'product_id':line.id,
                    'name':line.name,
                }))
            sale_order.update({'order_line':lines})