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
        copy=False, states={'done': [('readonly', True)]},
        compute='_compute_mrp_production_ids',
        groups='stock.group_stock_manager')

    @api.depends('date', 'date_to', 'company_id')
    def _compute_mrp_production_ids(self):
        for record in self:
            mrp_production_values = self.env['mrp.production']
            if record.date and record.date_to:
                mrp_production_values = mrp_production_values.search([
                    ('date_planned_start', '>=', record.date),
                    ('date_planned_start', '<=', record.date_to),
                    ('state', '=', 'done')
                ])
            if record.company_id:
                mrp_production_values = mrp_production_values.filtered(
                    lambda production: production.company_id.id == record.company_id.id
                )
            record.mrp_production_ids = mrp_production_values
            print("record.mrp_production_ids",record.mrp_production_ids)

    @api.onchange('date', 'date_to', 'company_id')
    def _onchange_date_range(self):
        domain_picking = []
        mrp_production_values = self.env['mrp.production']

        if self.date and self.date_to:
            domain_picking.append(('scheduled_date', '>=', self.date))
            domain_picking.append(('scheduled_date', '<=', self.date_to))


        if self.company_id:
            domain_picking.append(('company_id', '=', self.company_id.id))

        return {
            'domain': {
                'picking_ids': domain_picking,
            }
        }
