# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseWizard(models.TransientModel):
    _name = 'purchase.wizard'
    _description = 'Stock supplier replenishment information'


    vendor=  fields.Many2one('res.partner',  string="vendor" ,readonly=True)
    purchase_id=fields.Many2one('purchase.order')
    order_lines=fields.Many2many('purchase.wizard.line')

    def button_confirm(self):
        p = self.env['purchase.order'].search([
            ('id', '=', self.purchase_id.id)
        ])
        for s in self.order_lines:
            print('ososos',s)

        # for line in p.order_line :
        #     print('product',line.product_id)
        #     order = self.env['purchase.order.line'].search([
        #         ('partner_id', '=', self.vendor.id),
        #         ('product_id', '=', line.product_id.id)
        #     ], limit=1)
        #     print(order.price_unit)


        #
        for s in p:
            print('ssss', s)
            #
            return s.write({'state': 'purchase'})


    def cancel(self):
        print('ssss1')


        p= self.env['purchase.order'].search([
            ('id', '=', self.purchase_id.id)
        ])
        #
        for s in p:
           print('ssss',s)
        #
           return s.button_cancel()



    # supplierinfo_id = fields.Many2one(related='orderpoint_id.supplier_id')
    # supplierinfo_ids = fields.Many2many(
    #     'product.supplierinfo', compute='_compute_supplierinfo_ids',
    #     store=True)
    # vendor=fields.Many2one('')
    # @api.depends('orderpoint_id')
    # def _compute_supplierinfo_ids(self):
    #     for replenishment_info in self:
    #         replenishment_info.supplierinfo_ids = replenishment_info.product_id.seller_ids

# class tracking_validated_line_ids
class PurchaseWizerdLine(models.TransientModel):
    _name = 'purchase.wizard.line'


    product_id = fields.Many2one('product.product', 'Product')
    purchase_id=fields.Many2one('purchase.order')
    price_unit=fields.Float(string='Untit price')
