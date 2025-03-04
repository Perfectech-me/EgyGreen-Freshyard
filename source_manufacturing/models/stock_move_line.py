from odoo import fields, models, api

class StockMoveLineInherit(models.Model):
    _inherit = "stock.move.line"

    origin_id = fields.Many2one(
        'account.analytic.tag',
        string='Source Origin',

        readonly=False,
    )

    # @api.depends('move_id')
    # def _compute_origin_id(self):
    #     for line in self:
    #         if line.move_id and line.move_id.raw_material_production_id:
    #             print("line.move_id.raw_material_production_id.origin_id==",line.move_id.raw_material_production_id.origin_id)
    #             line.origin_id = line.move_id.raw_material_production_id.origin_id
    #         else:
    #             line.origin_id = False

