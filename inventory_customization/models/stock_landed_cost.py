from odoo import models, fields, api


class StockLandedCostInherit(models.Model):
    _inherit = 'stock.landed.cost'

    date = fields.Date(
        string='Date From',
        default=fields.Date.context_today,
        copy=False,
        required=True,
        states={'done': [('readonly', True)]},
        tracking=True
    )

    date_to = fields.Date(
        string='Date To',
        default=fields.Date.context_today,
        copy=False,
        required=True,
        states={'done': [('readonly', True)]},
        tracking=True
    )

    picking_ids = fields.Many2many(
        'stock.picking',
        string='Transfers',
        copy=False,
        states={'done': [('readonly', True)]}
    )
    mrp_production_ids = fields.Many2many(
        'mrp.production', string='Manufacturing order',
        copy=False, states={'done': [('readonly', True)]}, groups='stock.group_stock_manager')

    @api.onchange('date', 'date_to', 'company_id')
    def _onchange_date_range(self):
        domain_picking = []
        domain_mrp = []

        if self.date and self.date_to:
            domain_picking.append(('scheduled_date', '>=', self.date))
            domain_picking.append(('scheduled_date', '<=', self.date_to))

            domain_mrp.append(('date_planned_start', '>=', self.date))
            domain_mrp.append(('date_planned_start', '<=', self.date_to))

        if self.company_id:
            domain_picking.append(('company_id', '=', self.company_id.id))
            domain_mrp.append(('company_id', '=', self.company_id.id))
        domain_mrp.append(('state', '=', 'done'))

        return {
            'domain': {
                'picking_ids': domain_picking,
                'mrp_production_ids': domain_mrp,
            }
        }
