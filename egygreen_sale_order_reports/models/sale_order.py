from odoo import models, fields, api
from datetime import date,datetime
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    net_weight_per_unit = fields.Float(string="Net Weight Per Unit")
    gross_weight_per_unit = fields.Float(string="Gross Weight Per Unit")
    container_equipment_number = fields.Char(string="Container Equipment Number")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    partner_bank_id = fields.Many2one(comodel_name="res.partner.bank", string="Recipient Bank")
    data_loger = fields.Text(string="Data Loger")
    total_amount_egp = fields.Float(string="Total Amount EGP")



    @api.model
    def create(self, vals):
        result = super(SaleOrderInherit, self).create(vals)
        result._compute_total_amount_egp()
        return result

    def _compute_total_amount_egp(self):
        for rec in self:
            rec.total_amount_egp=0.0
            rates_current=[]
            rate=0
            if rec.currency_id:
                rates = rec.currency_id.rate_ids.mapped('name')
                for line in rates:
                    if line<=date.today():
                        rates_current.append(line)
                for line in rec.currency_id.rate_ids:
                    if max(set(rates_current))==line.name:
                        rate=line.inverse_company_rate
                if rate>0:
                    rec.total_amount_egp =rec.amount_total*rate
                else:
                    rec.total_amount_egp = rec.amount_total

class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    def create_invoices(self):
        res=super(SaleAdvancePaymentInvInherit, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if sale_orders:
            for sale in sale_orders:
                if sale.invoice_ids:
                    for inv in sale.invoice_ids:
                        inv.partner_bank_id=sale.partner_bank_id.id


        return res