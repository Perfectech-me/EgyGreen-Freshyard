from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

class Bom(models.TransientModel):
    _name = 'gogs_report_options'
    
    date_from = fields.Date()
    date_to = fields.Date()
    partner_ids = fields.Many2many('res.partner')
    analytic_account_ids = fields.Many2many('account.analytic.account')
    
    def get_domain(self):
        domain = [('state','=','posted'),('move_type','=','out_invoice')]
        if self.date_from and self.date_to:
            domain += [('invoice_date','>=',self.date_from),('invoice_date','<=',self.date_to)]
        if self.partner_ids:
            domain += [('partner_id','in',self.partner_ids.ids)]
        if self.analytic_account_ids:
            domain += [('sales_order_id.analytic_account_id','in',self.analytic_account_ids.ids)]
        return domain
    def print(self):
        orders = self.env['account.move'].search(self.get_domain())
        return self.env.ref('gogs_and_condition_report.gogs_xlsx').report_action(orders, data={})