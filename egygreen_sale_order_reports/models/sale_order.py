from odoo import models, fields, api
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    net_weight_per_unit = fields.Float(string="Net Weight Per Unit")
    gross_weight_per_unit = fields.Float(string="Gross Weight Per Unit")
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    partner_bank_id = fields.Many2one(comodel_name="res.partner.bank", string="Recipient Bank")