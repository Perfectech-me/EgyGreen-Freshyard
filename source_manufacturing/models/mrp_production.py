from odoo import api, fields, models, _


class MrpProductionInherit(models.Model):

    _inherit = "mrp.production"

    origin_id = fields.Many2one(
        'account.analytic.tag',
        string='Source Origin',
        copy=False,
        help="Reference of the document that generated this production order request."
    )

    def button_mark_done(self):
        res = super().button_mark_done()

        for production in self:
            all_move_lines = production.move_raw_ids.move_line_ids | production.move_finished_ids.move_line_ids
            print("all_move_liens",all_move_lines)
            all_move_lines.write({'origin_id': production.origin_id.id})

        return res

