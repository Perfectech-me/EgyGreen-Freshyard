from odoo import models, fields, api
from odoo.tests import Form

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'



    def button_add_product_additional_cost(self):
        lines=[]
        product_product_record=self.env['product.product'].search([('additional_service','=',True)])
        for line in product_product_record:
            lines.append((0, 0, {
                'product_id':line.id,
                'name':line.name,
            }))
        for order in self.order_line:
            if order.product_id.additional_service==True:
                order.unlink()
        self.update({'order_line':lines})



    def button_remove_product_additional_cost(self):
        for order in self.order_line:
            if order.product_id.additional_service==True:
                order.unlink()


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    additional_service = fields.Boolean(string="Additional Service")

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    service_provider_partner_id = fields.Many2one(comodel_name="res.partner", string="Service Provider" )
