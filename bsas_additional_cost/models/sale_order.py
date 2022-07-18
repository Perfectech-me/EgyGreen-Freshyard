from odoo import models, fields, api
from odoo.tests import Form

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'



    def button_add_product_additional_cost(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'product.additional.cost',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
        }


    def action_confirm(self):
        res=super(SaleOrderInherit, self).action_confirm()
        for rec in self:
            all_partners=[]
            for par in rec.order_line:
                all_partners.append(par.service_provider_partner_id.id)
            partners_records=self.env['res.partner'].search([('id','in',all_partners)])
            if partners_records:
                for partner in partners_records:
                    order_lines=[]
                    for line in rec.order_line:
                        if partner.id == line.service_provider_partner_id.id:
                            order_lines.append((0,0,{
                                'product_id':line.product_id.id,
                                'name':line.name,
                                'product_qty':line.product_uom_qty,
                                'price_unit':line.price_unit,
                                'taxes_id':line.tax_id.ids,
                            }))
                    self.env['purchase.order'].create({
                        'partner_id':partner.id,
                        'order_line':order_lines,

                    })

        return res


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    additional_service = fields.Boolean(string="Additional Service")

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    service_provider_partner_id = fields.Many2one(comodel_name="res.partner", string="Service Provider" )
