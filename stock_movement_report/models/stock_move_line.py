# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.float_utils import float_round


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    in_qty_available = fields.Float(string='IN', compute='_compute_qty_available')
    out_qty_available = fields.Float(string='OUT', compute='_compute_qty_available')
    qty_on_date = fields.Float(compute='_compute_qty_available', )
    balance_amount = fields.Float(compute='_compute_balance_amount', string='Balance')

    @api.depends('product_id', 'date')
    def _compute_qty_available(self):
        for line in self:
            qty_on_date = 0.0
            in_qty = 0.0
            out_qty = 0.0
            if line.product_id and line.date:
                product = line.product_id.with_context(to_date=line.date)
                qty_available = product.qty_available
                qty_on_date = float_round(qty_available, precision_rounding=line.product_uom_id.rounding)
            if line.move_id._is_in():
                in_qty = qty_on_date
            elif line.move_id._is_out():
                out_qty = qty_on_date
            elif line.move_id.picking_type_id.code == 'internal':
                in_qty = qty_on_date
                out_qty = qty_on_date

            line.qty_on_date = qty_on_date
            line.in_qty_available = in_qty
            line.out_qty_available = out_qty

    @api.depends('product_id', 'qty_on_date')
    def _compute_balance_amount(self):
        for line in self:
            line.balance_amount = line.product_id.standard_price * line.qty_on_date
