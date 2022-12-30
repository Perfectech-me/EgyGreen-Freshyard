from odoo import models, fields, api
class StockValuationLayerInherit(models.Model):

    _inherit = 'stock.valuation.layer'

    cost = fields.Float(string="Cost")#related='product_id.standard_price'

