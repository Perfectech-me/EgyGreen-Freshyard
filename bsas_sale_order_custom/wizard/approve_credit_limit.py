from odoo import models, fields, api

class ApproveCreditLimit(models.TransientModel):
    _name = 'approve.credit.limit'

    @api.model
    def default_get(self, fields):
        vals = super(ApproveCreditLimit, self).default_get(fields)
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids'))
        lines = []

        for line in sale_order.order_line:
            product_cost = line.product_id.standard_price
            balance=0.0
            account_move_line=self.env['account.move.line'].search([('full_reconcile_id', '=', False), ('balance', '!=', 0), ('account_id.reconcile', '=', True),('parent_state', '=', 'posted'),('account_id.internal_type', 'in', ['payable','receivable']),('partner_id', '=', line.service_provider_partner_id.id)])
            if line.product_id.additional_service:
                product_cost = line.price_unit
            for move_line in account_move_line:
                balance +=move_line.balance
            lines.append((0, 0, {
                'product_id': line.product_id.id,
                'cost': product_cost,
                'service_provider_partner_id': line.service_provider_partner_id.id,
                'balance':balance,
            }))


        vals['customer_credit_limit'] = sale_order.credit_limit_id
        vals['total_receivable'] = sale_order.total_receivable
        vals['amount_total'] = sale_order.amount_total
        vals['due_before'] = sale_order.total_receivable + sale_order.amount_total
        vals['blocking_limit'] = sale_order.partner_id.Blocking_limit
        vals['order_lines'] = lines



        return vals

    customer_credit_limit = fields.Float(string="Credit Limit", readonly=True)
    total_receivable = fields.Float(string="Total Receivable", readonly=True)
    due_before = fields.Float(string="Due after this Quotation", readonly=True)
    amount_total = fields.Float(string="Amount Total", readonly=True)
    blocking_limit = fields.Integer(string="Blocking Limit",readonly=True)

    order_lines = fields.One2many(comodel_name="sale.order.product", inverse_name="approve_credit_limit_id")

    def button_approve(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids'))
        sale_order.state = 'draft'

    def button_refuse(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids'))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'refuse.credit.limit',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context':{'default_sale_id':sale_order.id}
        }





class SaleOrderProduct(models.TransientModel):
    _name = 'sale.order.product'

    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    cost = fields.Float(string="Cost")
    service_provider_partner_id = fields.Many2one(comodel_name="res.partner", string="Service Provider")
    balance = fields.Float(string="Balance")
    approve_credit_limit_id = fields.Many2one(comodel_name="approve.credit.limit" )
