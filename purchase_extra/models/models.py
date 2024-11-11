import logging
from odoo import api, fields, models, _
from odoo.tools.misc import format_date

# from odoo.exceptions import UserError, ValidationError
#
# from odoo.tools.misc import format_date
# from odoo.osv import expression
# from datetime import date, datetime, timedelta
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
# from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    # l10n_cl_dte_email = fields.Char(string='DTE Email')
    # sss = fields.Char(string='Field1')
    commercial_register = fields.Char(string='Commercial Register')
    tax_commercial_name = fields.Char(string='Tax Commercial Name')
    tax_commercial_payer_name = fields.Char(string='Tax Commercial Payer Name')

    # sssss = fields.Char(string='Field3')

    # date_localization = fields.Date(string='Geolocation Date')


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'), ('purchase',)])

    def button_to_confirm(self):
        # self.write({
        #     'state': 'to approve',
        #
        # })
        # return res
        for order in self:
            if order.state in ['draft', 'sent']:
                order.state = 'to_approve'
            # order._add_supplier_to_product()
            # Deal with double validation process
            # if order._approval_allowed():
            #     order.button_approve()
            # else:
            #  order.write({'state': 'to_approve'})
            # if order.partner_id not in order.message_partner_ids:
            #     order.message_subscribe([order.partner_id.id])
        return True

    def button_to_approve(self):
        # res = super(PurchaseOrder, self).button_approve(force=force)

        view_id = self.env.ref('purchase_extra.wizard_view_form').id
        name = _(' ')
        # if self.env.context.get('carrier_recompute'):
        #     name = _('Update shipping cost')
        #     carrier = self.carrier_id
        # else:
        #     name = _('Add a shipping method')
        #     carrier = (
        #             self.with_company(self.company_id).partner_shipping_id.property_delivery_carrier_id
        #             or self.with_company(
        #         self.company_id).partner_shipping_id.commercial_partner_id.property_delivery_carrier_id
        #     )
        # p = self.env['purchase.order'].search([
        #     ('id', '=', self.purchase_id.id)
        # ])
        wizard_line_ids = []
        balance = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),

        ])
        total_balance = 0
        for r in balance:
            total_balance = total_balance + r.amount_total_signed

        print("total_payment", total_balance, self.partner_id.total_invoiced)

        for line in self.order_line:
            print('product', line.product_id)
            order = self.env['purchase.order.line'].search([
                # ('partner_id', '=', line.partner_id.id),
                ('product_id', '=', line.product_id.id),
                ('order_id', '!=', self.id)
            ], limit=1)
            print(order.price_unit, 'sssss')

            wizard_line_ids.append((0, 0, {
                'product_id': line.product_id.id,
                'purchase_id': order.order_id.id,

                'price_unit': order.price_unit,
                'product_quantity': line.product_id.qty_available,
                'balance': total_balance

            }))
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'purchase.wizard',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_vendor': self.partner_id.id,
                'default_purchase_id': self.id,
                'default_order_lines': wizard_line_ids
            }}
        # return {
        #     'name': 'name',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'choose.delivery.carrier',
        #     'view_id': view_id,
        #     'views': [(view_id, 'form')],
        #     'target': 'new',
        #     'context': {
        #         'default_vendor': self.id,
        #         # 'default_carrier_id': carrier.id,
        #     }

        # return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_qty_percentage = fields.Float('Qty percentage', compute='get_product_qty_percentage')
    estimate_unit_price = fields.Float('Estimate price')
    estimate_subtotal = fields.Float('Estimate subtotal')

    @api.depends('order_id', 'product_id', 'product_qty')
    def get_product_qty_percentage(self):
        for rec in self:
            rec.product_qty_percentage = 0
            qty_total = sum(line.product_qty for line in rec.order_id.order_line)
            for order in rec.order_id.order_line:
                if qty_total > 0:
                    order.product_qty_percentage = order.product_qty / qty_total

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'estimate_unit_price': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date,
                                                             round=False),
            'estimate_subtotal': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date,
                                                           round=False) * self.qty_to_invoice,
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'purchase_line_id': self.id,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res

    @api.onchange('estimate_unit_price', 'product_qty')
    def _compute_percentage(self):
        qty_total = 0
        # for order in self:
        self.estimate_subtotal = self.estimate_unit_price * self.product_qty


class AccountMove(models.Model):
    _inherit = 'account.move'

    bill_description = fields.Text('Bill Description')
    vendor_invoice = fields.Selection([('copy', 'Copy'), ('original', 'Original')],
                                      string='Vendor Invoice', default='copy')
    bill_type = fields.Selection([('actual', 'Actual'), ('estimate', 'Estimate')],
                                 string='Bill Type', default='estimate')

    ref = fields.Char(string='Bill Reference', copy=False)

    @api.constrains('ref')
    def _check_unique_ref(self):
        for record in self:
            if record.ref:
                existing_move = self.search([('ref', '=', record.ref), ('id', '!=', record.id)], limit=1)
                if existing_move:
                    raise ValidationError("The Bill Reference must be unique")

    @api.onchange('invoice_line_ids')
    def _bill_type(self):
        for rec in self:
            rec.bill_type = 'actual'

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        for r in vals_list:
            print("rrrrrrrrrrrrrrrr", r)

        vals_list = self._move_autocomplete_invoice_lines_create(vals_list)
        return super(AccountMove, self).create(vals_list)


class AccountPartnerLedger(models.AbstractModel):
    _inherit = 'account.partner.ledger'

    def _get_columns_name(self, options):
        columns = [
            {},
            {'name': _('JRNL')},
            {'name': _('Account')},
            {'name': _('Desc')},
            {'name': _('Ref')},
            {'name': _('Due Date'), 'class': 'date'},
            {'name': _('Matching Number')},
            {'name': _('Initial Balance'), 'class': 'number'},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'}]

        if self.user_has_groups('base.group_multi_currency'):
            columns.append({'name': _('Amount Currency'), 'class': 'number'})

        columns.append({'name': _('Balance'), 'class': 'number'})

        return columns

    @api.model
    def _get_report_line_move_line(self, options, partner, aml, cumulated_init_balance, cumulated_balance):
        if aml['payment_id']:
            caret_type = 'account.payment'
        elif aml['move_type'] in ('in_refund', 'in_invoice', 'in_receipt'):
            caret_type = 'account.invoice.in'
        elif aml['move_type'] in ('out_refund', 'out_invoice', 'out_receipt'):
            caret_type = 'account.invoice.out'
        else:
            caret_type = 'account.move'

        date_maturity = aml['date_maturity'] and format_date(self.env,
                                                             fields.Date.from_string(aml['date_maturity']))

        # aml_id = self.env['account.move'].browse(int(aml['id']))
        # bill_description = aml_id.bill_description or '

        aml_id = self.env['account.move'].search_read([('name', '=', aml['move_name'])])

        # bill_des=a['bill_description']
        for a in aml_id:
            # print('ididid',aml_id.bill_description)
            # bill_description = aml_id.bill_description or ''
            columns = [
                {'name': aml['journal_code']},
                {'name': aml['account_code']},
                {'name': a['bill_description']},
                {'name': self._format_aml_name(aml['name'], aml['ref'], aml['move_name'])},
                {'name': date_maturity or '', 'class': 'date'},
                {'name': aml['matching_number'] or ''},
                {'name': self.format_value(cumulated_init_balance), 'class': 'number'},
                {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
                {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
            ]

        if self.user_has_groups('base.group_multi_currency'):
            if aml['currency_id']:
                currency = self.env['res.currency'].browse(aml['currency_id'])
                formatted_amount = self.format_value(aml['amount_currency'], currency=currency, blank_if_zero=True)
                columns.append({'name': formatted_amount, 'class': 'number'})
            else:
                columns.append({'name': ''})
        columns.append({'name': self.format_value(cumulated_balance), 'class': 'number'})
        return {
            'id': aml['id'],
            'parent_id': 'partner_%s' % (partner.id if partner else 0),
            'name': format_date(self.env, aml['date']),
            'class': 'text' + aml.get('class', ''),  # do not format as date to prevent text centering
            'columns': columns,
            'caret_options': caret_type,
            'level': 2,
        }

    #
    # @api.model
    # def _get_report_line_move_line(self, options, partner, aml, cumulated_init_balance, cumulated_balance):
    #     if aml['payment_id']:
    #         caret_type = 'account.payment'
    #     elif aml['move_type'] in ('in_refund', 'in_invoice', 'in_receipt'):
    #         caret_type = 'account.invoice.in'
    #     elif aml['move_type'] in ('out_refund', 'out_invoice', 'out_receipt'):
    #         caret_type = 'account.invoice.out'
    #     else:
    #         caret_type = 'account.move'
    #
    #     date_maturity = aml['date_maturity'] and format_date(self.env,
    #                                                          fields.Date.from_string(aml['date_maturity']))
    #
    #     aml_id = self.env['account.move'].browse(int(aml['id']))
    #     bill_description = aml_id.bill_description or ''
    #     columns = [
    #         {'name': aml['journal_code']},
    #         {'name': aml['account_code']},
    #         {'name': bill_description},
    #         {'name': self._format_aml_name(aml['name'], aml['ref'], aml['move_name'])},
    #         {'name': date_maturity or '', 'class': 'date'},
    #         {'name': aml['matching_number'] or ''},
    #         {'name': self.format_value(cumulated_init_balance), 'class': 'number'},
    #         {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
    #         {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
    #     ]
    #     if self.user_has_groups('base.group_multi_currency'):
    #         if aml['currency_id']:
    #             currency = self.env['res.currency'].browse(aml['currency_id'])
    #             formatted_amount = self.format_value(aml['amount_currency'], currency=currency, blank_if_zero=True)
    #             columns.append({'name': formatted_amount, 'class': 'number'})
    #         else:
    #             columns.append({'name': ''})
    #     columns.append({'name': self.format_value(cumulated_balance), 'class': 'number'})
    #
    #     return {
    #         'id': aml['id'],
    #         'parent_id': 'partner_%s' % (partner.id if partner else 0),
    #         'name': format_date(self.env, aml['date']),
    #         'class': 'text' + aml.get('class', ''),  # do not format as date to prevent text centering
    #         'columns': columns,
    #         'caret_options': caret_type,
    #         'level': 2,
    #     }

    @api.model
    def _get_report_line_total(self, options, initial_balance, debit, credit, balance):
        columns = [
            {'name': ''},
            {'name': self.format_value(initial_balance), 'class': 'number'},
            {'name': self.format_value(debit), 'class': 'number'},
            {'name': self.format_value(credit), 'class': 'number'},
        ]
        if self.user_has_groups('base.group_multi_currency'):
            columns.append({'name': ''})
        columns.append({'name': self.format_value(balance), 'class': 'number'})
        return {
            'id': 'partner_ledger_total_%s' % self.env.company.id,
            'name': _('Total'),
            'class': 'total',
            'level': 1,
            'columns': columns,
            'colspan': 6,
        }

    @api.model
    def _get_report_line_partner(self, options, partner, initial_balance, debit, credit, balance):
        company_currency = self.env.company.currency_id
        unfold_all = self._context.get('print_mode') and not options.get('unfolded_lines')

        columns = [
            {'name': ''},
            {'name': self.format_value(initial_balance), 'class': 'number'},
            {'name': self.format_value(debit), 'class': 'number'},
            {'name': self.format_value(credit), 'class': 'number'},
        ]
        if self.user_has_groups('base.group_multi_currency'):
            columns.append({'name': ''})
        columns.append({'name': self.format_value(balance), 'class': 'number'})

        return {
            'id': 'partner_%s' % (partner.id if partner else 0),
            'partner_id': partner.id if partner else None,
            'name': partner is not None and (partner.name or '')[:128] or _('Unknown Partner'),
            'columns': columns,
            'level': 2,
            'trust': partner.trust if partner else None,
            'unfoldable': not company_currency.is_zero(debit) or not company_currency.is_zero(credit),
            'unfolded': 'partner_%s' % (partner.id if partner else 0) in options['unfolded_lines'] or unfold_all,
            'colspan': 6,
        }
    # @api.onchange('invoice_line_ids')
    # def set_line_ids(self):
    #     #inherit of the function from account.move to validate a new tax and the priceunit of a downpayment
    #     subtotal=0
    #     for r in self.invoice_line_ids:
    #         subtotal=subtotal + r.price_subtotal
    #     for r in self.line_ids:
    #         if r.debit>0:
    #             r.debit=subtotal
    #         if r.credit>0:
    #             r.credit=subtotal
    #         print("rrrrrr",r.debit)
    # res = super(AccountMove, self).action_post()
    # return res


class AccountMoveLine(models.Model):
    """ Override AccountInvoice_line to add the link to the purchase order line it is related to"""
    _inherit = 'account.move.line'

    estimate_unit_price = fields.Float('estimate price')
    estimate_subtotal = fields.Float('estimate subtotal')
#
