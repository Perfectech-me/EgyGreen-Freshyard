from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    net_weight_per_unit = fields.Float(string="Net Weight Per Unit")
    gross_weight_per_unit = fields.Float(string="Gross Weight Per Unit")
    container_equipment_number = fields.Char(string="Container Equipment Number")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    no_of_pallets = fields.Char(string="No of Pallets")
    no_of_cartons = fields.Char(string="No of Cartons")
    hs_code = fields.Char(string="HS Code")
    ip_number = fields.Char(string="IP Number")
    irc_no = fields.Char(string="IRC No")
    partial_shipments = fields.Char(string="Partial Shipments")
    transshipment = fields.Char(string="Transshipment")
    lc_no = fields.Char(string="LC No")
    lc_date = fields.Char(string="LC Date")
    lcaf_no = fields.Char(string="LCAF No")
    partner_bank_id = fields.Many2one(comodel_name="res.partner.bank", string="Recipient Bank")
    data_loger = fields.Text(string="Data Loger")
    total_amount_egp = fields.Float(string="Total Amount EGP")
    container_equipment_number = fields.Char(string="Container Equipment Number")

    def _prepare_invoice(self):
        self.ensure_one()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(
                _('Please define an accounting sales journal for the company %s (%s).', self.company_id.name,
                  self.company_id.id))

        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(
                self.partner_invoice_id.id)).id,
            'partner_bank_id': self.company_id.partner_id.bank_ids.filtered(
                lambda bank: bank.company_id.id in (self.company_id.id, False))[:1].id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,

            # Include your custom fields here
            'no_of_pallets': self.no_of_pallets,
            'no_of_cartons': self.no_of_cartons,
            'hs_code': self.hs_code,
            'ip_number': self.ip_number,
            'irc_no': self.irc_no,
            'partial_shipments': self.partial_shipments,
            'transshipment': self.transshipment,
            'lc_no': self.lc_no,
            'lc_date': self.lc_date,
            'lcaf_no': self.lcaf_no,
        }
        return invoice_vals

    @api.model
    def create(self, vals):
        result = super(SaleOrderInherit, self).create(vals)
        result._compute_total_amount_egp()
        return result

    def _compute_total_amount_egp(self):
        for rec in self:
            rec.total_amount_egp = 0.0
            rates_current = []
            rate = 0
            if rec.currency_id:
                rates = rec.currency_id.rate_ids.mapped('name')
                for line in rates:
                    if line <= date.today():
                        rates_current.append(line)
                for line in rec.currency_id.rate_ids:
                    if max(set(rates_current)) == line.name:
                        rate = line.inverse_company_rate
                if rate > 0:
                    rec.total_amount_egp = rec.amount_total * rate
                else:
                    rec.total_amount_egp = rec.amount_total


class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        res = super(SaleAdvancePaymentInvInherit, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if sale_orders:
            for sale in sale_orders:
                if sale.invoice_ids:
                    for inv in sale.invoice_ids:
                        inv.partner_bank_id = sale.partner_bank_id.id

        return res
