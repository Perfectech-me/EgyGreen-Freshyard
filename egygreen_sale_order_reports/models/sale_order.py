from odoo import models, fields, api
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    net_weight_per_unit = fields.Float(string="Net Weight Per Unit")
    gross_weight_per_unit = fields.Float(string="Gross Weight Per Unit")
    container_equipment_number = fields.Char(string="Container Equipment Number")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    partner_bank_id = fields.Many2one(comodel_name="res.partner.bank", string="Recipient Bank")
    data_loger = fields.Text(string="Data Loger")


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