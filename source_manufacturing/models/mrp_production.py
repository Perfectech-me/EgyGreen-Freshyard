from odoo import api, fields, models, _


class MrpProductionInherit(models.Model):

    _inherit = "mrp.production"

    origin_id = fields.Many2one(
        'account.analytic.tag',
        string='Source Origin',
        copy=False,
        help="Reference of the document that generated this production order request."
    )

