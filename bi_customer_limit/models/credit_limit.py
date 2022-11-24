# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import werkzeug.urls

class res_pertner(models.Model):
    _inherit = "res.partner"
    
    credit_limit = fields.Integer(string="Credit Limit")
    credit_on_hold = fields.Boolean(string="Put on Hold")

    Blocking_limit = fields.Integer(string="Blocking Limit")
    is_credit_limit = fields.Boolean(String="Active Credit Limit")
    balance_invoice_ids = fields.One2many('account.move', 'partner_id', 'Customer move lines', domain=[('move_type', 'in', ['out_invoice','out_refund']),('payment_state', 'not in', ['paid']),('state','=','posted')]) 
    customer_due_amt = fields.Float("Customer Due Amount",compute="depends_partner_id",store=True, copy=False)



    @api.depends('balance_invoice_ids')
    def depends_partner_id(self):
        for partner in self:
            supplier_amount_due = 0.0
            if partner:
                for aml in partner.balance_invoice_ids:
                    supplier_amount_due += aml.result
            partner.update({
                'customer_due_amt' : supplier_amount_due
            }) 

class acc_invoice(models.Model):

    _inherit = 'account.move'
    
    
    def _get_result(self):
        for aml in self:
            credit_amount = result = 0.0
            credit_amount = aml.amount_total_signed - aml.amount_residual_signed
            result = aml.amount_total_signed - credit_amount
            
            aml.update({
                'credit_amount' : credit_amount,
                'result' : result,
                })


    credit_amount = fields.Float(compute ='_get_result',  string="Credit/paid")
    result = fields.Float(compute ='_get_result',  string="Balance")


class sale_order(models.Model):
    _inherit = "sale.order"
    
    credit_limit_id = fields.Integer(string="Credit Limit")
    total_receivable = fields.Float(string="Total Receivable", compute="_compute_total_receivable")
    exceeded_amount = fields.Float(string="Exceeded Amount")
    sale_url = fields.Char(string="url", compute="_compute_total_receivable")
    customer_due_amt = fields.Float("Customer Due Amount",compute="depends_partner_id",store=True, copy=False)
    is_confirm = fields.Boolean(string="Is Confirm",default=False, copy=False)
    is_warning = fields.Boolean(string="Is Warning",default=False, copy=False)
    

    def _compute_total_receivable(self):
        for order in self:

            if order.partner_id.credit:
                order.update({'total_receivable' : self.partner_id.credit})
            if not order.partner_id.credit:
                order.update({'total_receivable' : self.partner_id.parent_id.credit})

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            static_url = "/web"
            view_id = "?db=%s#id=%s" % (self._cr.dbname, self.id)
            view_type = "&view_type=form&model=sale.order"
            sale_url_id = str(base_url) + static_url + view_id + view_type

            order.update({
                'sale_url' : sale_url_id
            })

    @api.depends('partner_id')
    def depends_partner_id(self):
        for order in self:
            supplier_amount_due = 0.0
            if order.partner_id:
                for aml in order.partner_id.balance_invoice_ids:
                    supplier_amount_due += aml.result
            order.update({
                'customer_due_amt' : supplier_amount_due
            })

    @api.constrains("total_receivable", "partner_id",'amount_total')
    def _check_Blocking_limit(self):
        if self.partner_id.is_credit_limit and self.partner_id.Blocking_limit <= (self.total_receivable+self.amount_total):
            raise ValidationError(_("The Customer is in blocking stage "))

    @api.model
    def create(self, vals):
        partner_id= False
        if 'partner_id' in vals:
            partner_id = self.env['res.partner'].browse(vals['partner_id'])

        if partner_id.Blocking_limit != 0.0:
            if partner_id.Blocking_limit < partner_id.customer_due_amt:
                raise ValidationError(_('The Customer is in blocking stage and has to pay '+str(partner_id.customer_due_amt)))
        result = super(sale_order, self).create(vals)
        return result

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.update({
                'partner_invoice_id' : False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        if not self.partner_id.credit:
            self.partner_id.credit = self.partner_id.parent_id.credit
            
        addr = self.partner_id.address_get(['delivery', 'invoice'])

        vals = {
            'pricelist_id' : self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id' : self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'credit_limit_id': self.partner_id.credit_limit,
            'total_receivable': self.partner_id.credit,
            }

        if self.partner_id.user_id:
            vals['user_id'] = self.partner_id.user_id.id
        if self.partner_id.team_id:
            vals['team_id'] = self.partner_id.team_id.id
        
        if self.partner_id.is_credit_limit == True:
            if self.customer_due_amt > self.partner_id.credit_limit:
                self.is_warning = True
            else:
                self.is_warning = False
        else:
            self.is_warning = False
        self.update(vals)

    def action_confirm(self):
        if self.partner_id.is_credit_limit == False:
            res = super(sale_order, self).action_confirm()
            return res
        else:
            if self.is_confirm == True:
                res = super(sale_order, self).action_confirm()
                return res
            else:
                partner = self.partner_id
                account_move_line = self.env['account.move.line']
                if partner.is_company:
                    account_move_line = account_move_line.\
                        search([('partner_id', '=', partner.id),
                                ('account_id.user_type_id.name', 'in',
                                 ['Receivable', 'Payable'])
                                ])
                if not partner.is_company:
                    account_move_line = account_move_line.\
                        search([('partner_id', '=', partner.parent_id.id),
                                ('account_id.user_type_id.name', 'in',
                                 ['Receivable', 'Payable'])
                                ])
                    self.partner_id.credit_on_hold = self.partner_id.parent_id.credit_on_hold
                    
                credit = 0.0
                debit = 0.0
                
                for line in account_move_line:
                    credit += line.credit
                    debit += line.debit
                
                total = debit - credit + self.amount_total
                self.exceeded_amount = self.total_receivable - self.credit_limit_id + self.amount_total
                self.sale_url = self.sale_url
                for order in self:
                    order.write({
                        'exceeded_amount' : self.exceeded_amount,
                        'credit_limit_id' : self.credit_limit_id,
                    })
                    
                    if self.partner_id.credit_on_hold is False:
                        if (total) > partner.credit_limit:
                            wizard_credit_limit_obj = self.env.ref('bi_customer_limit.view_wizard_credit_limit_form')
                            limit = {}
                            if wizard_credit_limit_obj:
                                limit = {
                                    'name' : _('Credit Limit'),
                                    'type' : 'ir.actions.act_window',
                                    'view_type' : 'form',
                                    'view_mode' : 'form',
                                    'res_model' : 'wizard_custom_credit',
                                    'view_id' : wizard_credit_limit_obj.id,
                                    'target' : 'new',
                                    'context' : {
                                        'default_sale_id' : self.id,
                                        'sale_order_name' : self.name,
                                        'amount_total' : self.amount_total,
                                        'credit_limit_id' : self.credit_limit_id,
                                        'default_partner_id_credit' : self.partner_id.credit,
                                        'default_partner_id_name' : self.partner_id.name,
                                        'total_recievable' : self.total_receivable,
                                    },
                                }
                                return limit
                        else:
                            order.write({
                                'credit_limit_id':partner.credit_limit
                            })
                            res = super(sale_order, self).action_confirm()
                        return True
                    else:
                        raise ValidationError(_('You have been put on hold due to exceeding your credit limit. Please contact administration for further guidance. \n Thank You'))
                        return False