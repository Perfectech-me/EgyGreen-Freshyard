# -*- coding: utf-8 -*-
from num2words import num2words

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta


class account_cheque(models.Model):
    _name = 'account.cheque'
    _description = 'Account Cheque'

    _rec_name = 'sequence'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    sequence = fields.Char(string='ٍSequence', required=True, copy=False, store=True, index=True,
                           default=lambda self: self.env['ir.sequence'].next_by_code('cheque'))

    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account")

    total_amount_arabic_word = fields.Char(string="Arabic Amount", compute='compute_amount_arabic_word')

    @api.depends('amount','currency_id')
    def compute_amount_arabic_word(self):
        for rec in self:
            if rec.currency_id:
                rec.total_amount_arabic_word = ''
                amount = round(rec.amount, 4)
                text = rec.currency_id.amount_to_text(amount)
                integer = int(amount)
                decimal = round((amount - integer), 2) * 100
                riyal = num2words(integer, lang='ar')
                halala = num2words(decimal, lang='ar')
                text_ar = riyal
                text_ar += " " + str(rec.currency_id.currency_unit_arabic)
                if decimal:
                    text_ar += ' و'
                    text_ar += halala
                    text_ar += " " + str(rec.currency_id.currency_subunit_arabic)

                    # total_amount=str(text_ar).split()
                amount_text = text_ar
                line_list = str(text_ar).split()
                if 'عشرين' in line_list:
                    amount_text = str(str(text_ar).replace("عشرين", "عشرون"))

                if 'وعشرين' in line_list:
                    amount_text = str(str(text_ar).replace("وعشرين", "وعشرون"))

                if 'ثلاثين' in line_list:
                    amount_text = str(str(text_ar).replace("ثلاثين", "ثلاثون"))

                if 'وثلاثين' in line_list:
                    amount_text = str(str(text_ar).replace("وثلاثين", "وثلاثون"))

                if 'أربعين' in line_list:
                    amount_text = str(str(text_ar).replace("أربعين", "أربعون"))
                if 'وأربعين' in line_list:
                    amount_text = str(str(text_ar).replace("وأربعين", "وأربعون"))

                if 'خمسين' in line_list:
                    amount_text = str(str(text_ar).replace("خمسين", "خمسون"))
                if 'وخمسين' in line_list:
                    amount_text = str(str(text_ar).replace("وخمسين", "وخمسون"))

                if 'ستين' in line_list:
                    amount_text = str(str(text_ar).replace("ستين", "ستون"))
                if 'وستين' in line_list:
                    amount_text = str(str(text_ar).replace("وستين", "وستون"))

                if 'سبعين' in line_list:
                    amount_text = str(str(text_ar).replace("سبعين", "سبعون"))
                if 'وسبعين' in line_list:
                    amount_text = str(str(text_ar).replace("وسبعين", "وسبعون"))

                if 'ثمانين' in line_list:
                    amount_text = str(str(text_ar).replace("ثمانين", "ثمانون"))

                if 'وثمانين' in line_list:
                    amount_text = str(str(text_ar).replace("وثمانين", "وثمانون"))

                if 'تسعين' in line_list:
                    amount_text = str(str(text_ar).replace("تسعين", "تسعون"))

                if 'وتسعين' in line_list:
                    amount_text = str(str(text_ar).replace("وتسعين", "وتسعون"))
                if 'مئة' in amount_text:
                    amount_text = str(str(amount_text).replace("مئة", "مائة"))
                if 'ومئة' in amount_text:
                    amount_text = str(str(amount_text).replace("ومئة", "ومائة"))

                if 'مئتين' in amount_text:
                    amount_text = str(str(amount_text).replace("مئتين", "مائتين"))
                if 'ومئتين' in amount_text:
                    amount_text = str(str(amount_text).replace("ومئتين", "ومائتين"))

                if '،' in amount_text:
                    amount_text = str(str(amount_text).replace("،", ","))

                rec.total_amount_arabic_word = amount_text

    def _get_report_base_filename(self):
        return self.name

    @api.model
    def create(self, waltz):

        account_type_test=self.env['account.account'].search_read([])
        for a in account_type_test:
            print('a.type',a)
        if waltz:
            waltz['sequence'] = self.env['ir.sequence'].next_by_code('cheque')
            print(waltz['sequence'])
        return super(account_cheque, self).create(waltz)
    type = fields.Selection(string="", selection=[('incoming', 'incoming'), ('outgoing', 'outgoing'), ],
                            required=True, )
    name = fields.Char(string="Name", required=True, )
    bank_account_id = fields.Many2one(comodel_name="account.account", string="Bank Account", required=True,  domain=[('user_type_id', '=',  'Bank and Cash')] )
    payer_user_id = fields.Many2one(comodel_name="res.partner", string="Payer", required=False, )
    payee_user_id = fields.Many2one(comodel_name="res.partner", string="Payee", required=False, )
    chq_no = fields.Char(string="Cheque Number", required=True, )
    cheque_date = fields.Date(string="Cheque Date", required=True, )
    payer_bank = fields.Text(string="Payer Bank", required=False, )
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True,default=lambda self: self.env.company.id)
    amount = fields.Float(string="Amount", required=True, )
    amount_egy = fields.Float(string="Amount EGY",compute='compute_amount_egy')


    cheque_given_date = fields.Date(string="Cheque Given Date", required=False, )
    cheque_receive_date = fields.Date(string="", required=False, )
    cheque_return_date = fields.Date(string="", required=False, )
    journal_id = fields.Many2one(comodel_name="account.journal", string="Journal" , required=True, )
    credit_account_id = fields.Many2one(comodel_name="account.account", string="Credit Account", required=True, )
    debit_account_id = fields.Many2one(comodel_name="account.account", string="Debit Account", required=True, )
    cheq_under_collection_account_id = fields.Many2one(comodel_name="account.account",
                                                       string="Cheque Under Collection Account", required=False, )
    comment = fields.Text(string="", required=False, )
    invoice_ids = fields.One2many(comodel_name="account.move", inverse_name="chq_id", string="", required=False)
    bills_ids = fields.One2many(comodel_name="account.move", inverse_name="chq_id", string="", required=False)
    status = fields.Selection(string="",
                              selection=[('draft', 'Draft'), ('registered', 'Registered'), ('bank', 'Bank Repository'),
                                         ('bounced', 'Bounced'),
                                         ('done', 'Done'), ('cancel', 'Cancel'), ], required=False, default='draft')
    current_state_date = fields.Date(string="Current State Date", required=False, default=datetime.today().date())
    journal_items_count = fields.Integer(string="", required=False, )
    attachment = fields.Many2many('ir.attachment')
    current_state_date = fields.Date(string="Current State Date", required=False, default=datetime.today().date())
    beneficiary_name = fields.Char(string="إسم المستفيد")

    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")

    @api.depends('amount','currency_id')
    def compute_amount_egy(self):
        for rec in self:
            if rec.currency_id.rate>0 and rec.currency_id.id != self.env.ref('base.EGP').id:
                rec.amount_egy=rec.amount / rec.currency_id.rate
            else:
                rec.amount_egy =rec.amount

    def check_company(self):
        res={}
        for rec in self:
            rec.company_id = ""

            com = self.env['res.company'].browse(self._context.get('allowed_company_ids')).ids
            domain = [('id', 'in', com)]
            res['domain'] = {'company_id': domain}
        print(self.env['res.company'].search([]))

        for rec in self.env.company:
            print('rec',rec)
        return res


    @api.constrains('chq_no')
    def _chq_no_constraint(self):
        if self.chq_no:
            for sympol in self.chq_no:
                print(sympol)
                if sympol not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                    raise ValidationError('Your Cheque Number Must Be Only Numbers !')

    @api.constrains('cheque_return_date')
    def _return_date_constraint(self):
        if self.type == 'incoming':
            if self.cheque_return_date:
                if self.cheque_return_date < self.cheque_receive_date or self.cheque_return_date < self.cheque_date:
                    raise ValidationError('Your return date before receive date !')
        else:
            if self.cheque_return_date:
                if self.cheque_return_date < self.cheque_given_date or self.cheque_return_date < self.cheque_date:
                    raise ValidationError('Your return date before given date !')

    @api.constrains('cheque_receive_date')
    def _receive_date_constraint(self):
        if self.cheque_receive_date:
            if self.cheque_receive_date > datetime.today().date():
                raise ValidationError('your receive date after today !')

    @api.constrains('cheque_given_date')
    def _given_date_constraint(self):
        if self.cheque_given_date:
            if self.cheque_given_date > datetime.today().date():
                raise ValidationError('your given date after today !')

    def unlink(self):
        if self.status != 'draft':
            raise ValidationError('This Cheque Cannot be deleted as its state not draft')
        return super(account_cheque, self).unlink()

    @api.onchange('payer_user_id')
    def get_partner_invoices_payer(self):
        if self.payer_user_id:
            x = self.env['account.move'].search(
                [('partner_id', '=', self.payer_user_id.id), ('move_type', '=', 'out_invoice')])
            print(x)
            self.invoice_ids = x

    @api.onchange('payee_user_id')
    def get_partner_invoices_payee(self):
        if self.payee_user_id:
            x = self.env['account.move'].search(
                [('partner_id', '=', self.payee_user_id.id), ('move_type', '=', 'in_invoice')])
            self.bills_ids = x

    def action_view_jornal_items(self):
        return {
            'name': 'Journal Items',
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'domain': [('move_id.cheque_id', '=', self.id)]}

    _sql_constraints = [
        ('ch_no_uni', 'UNIQUE (chq_no)', 'Cheque Number Must Be Unique')
    ]

    def set_to_submit(self):
        if self.amount <= 0:
            raise ValidationError('Your Cheque Amount Cannot Be 0.0 !')
        if int(self.chq_no) <= 0:
            raise ValidationError('Your Cheque Number Cannot Be 0.0 !')
        self.status = 'registered'
        if self.type == 'incoming':
            x = self.payer_user_id
            date = self.cheque_receive_date
        else:
            x = self.payee_user_id
            date = self.cheque_given_date
        self.journal_items_count += 2
        self.current_state_date = datetime.today().strftime('%Y-%m-%d')
        records = []

        if self.currency_id.id==self.company_id.currency_id.id:
            debit=self.amount
            credit=self.amount
        else:
            if self.debit_account_id.currency_id.rate>0:
                debit=self.amount / self.debit_account_id.currency_id.rate
            else:
                debit=0
            if self.debit_account_id.currency_id.rate>0:
                credit=self.amount / self.debit_account_id.currency_id.rate
            else:
                credit=0
        object1 = (
            0, 0, {
                'name': self.name,
                'account_id': self.debit_account_id.id,
                'debit': debit,
                'amount_currency': self.amount ,
                'credit': 0.0,
                'journal_id': self.journal_id.id,
                'partner_id': x.id,
                'analytic_account_id': self.analytic_account_id.id,
                'currency_id': self.debit_account_id.currency_id.id,
            })
        object2 = (
            0, 0, {'name': self.name,
                   'account_id': self.credit_account_id.id,
                   'debit': 0.0,
                   'credit': credit,
                   'amount_currency': -self.amount,
                   'journal_id': self.journal_id.id,
                   'partner_id': x.id,
                   'analytic_account_id': self.analytic_account_id.id,
                   'currency_id': self.credit_account_id.currency_id.id,

                   })

        records.append(object1)
        records.append(object2)
        move_vals = {
            'ref': self.sequence + '- Registered',
            'move_type': 'entry',
            'date': date,
            'journal_id': self.journal_id.id,
            'line_ids': records,
            'state': 'draft',
            'cheque_id': self.id
        }
        self.env['account.move'].create(move_vals)

    def set_cashed(self):
        if self.type == 'incoming':
            self.status = 'done'
            x = self.payer_user_id
            debit = self.bank_account_id
            credit = self.debit_account_id
            if(self.journal_items_count==4):
               credit = self.cheq_under_collection_account_id
            print("self.debit_account_id",self.debit_account_id.name,"self.debit_account_id",self.credit_account_id.name)

            self.journal_items_count += 2
            self.current_state_date = datetime.today().strftime('%Y-%m-%d')
            records = []
            object1 = (
                0, 0, {
                    'name': self.name,
                    'account_id': debit.id,
                    'debit': self.amount,
                    'credit': 0.0,
                    'journal_id': self.journal_id.id,
                    'partner_id': x.id,
                    # 'currency_id': self.currency_id.id,
                })
            object2 = (
                0, 0, {'name': self.name,
                       'account_id': credit.id,
                       'debit': 0.0,
                       'credit': self.amount,
                       'journal_id': self.journal_id.id,
                       'partner_id': x.id,
                       })

            records.append(object1)
            records.append(object2)
            move_vals = {
                'ref': self.sequence + '- Cashed',
                'date': self.cheque_receive_date,
                'journal_id': self.journal_id.id,
                'line_ids': records,
                'state': 'draft',
                'move_type':'entry',
                'cheque_id': self.id
            }
            self.env['account.move'].create(move_vals)
        else:
            self.current_state_date = datetime.today().strftime('%Y-%m-%d')
            return {
                'name': 'Cheque',
                'view_mode': 'form',
                'res_model': 'cashed.wizard',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {
                    'default_cheque_id': self.id,
                }}

    def set_to_bank(self):
        self.status = 'bank'
        print(self.cheq_under_collection_account_id)
        if self.type == 'incoming':
            x = self.payer_user_id
            date = self.cheque_receive_date
        else:
            x = self.payee_user_id
            date = self.cheque_given_date
        self.journal_items_count += 2
        self.current_state_date = datetime.today().strftime('%Y-%m-%d')
        records = []
        object1 = (
            0, 0, {
                'name': self.name,
                'account_id': self.debit_account_id.id,
                'debit': 0.0,
                'credit': self.amount,
                'journal_id': self.journal_id.id,
                'partner_id': x.id,
                # 'currency_id': self.currency_id.id,
            })
        object2 = (
            0, 0, {'name': self.name,
                   'account_id': self.cheq_under_collection_account_id.id,
                   'debit': self.amount,
                   'credit': 0.0,
                   'journal_id': self.journal_id.id,
                   'partner_id': x.id,
                   })

        records.append(object1)
        records.append(object2)
        move_vals = {
            'ref': self.sequence + '- Bank Repository',
            'date': date,
            'journal_id': self.journal_id.id,
            'line_ids': records,
            'state': 'draft',
            'cheque_id': self.id,
            'move_type': 'entry',

        }
        self.env['account.move'].create(move_vals)

    def open_payment_matching_screen(self):
        # Open reconciliation view for customers/suppliers
        move_line_id = False
        x = self.env['account.move.line'].search([('move_id.cheque_id', '=', self.id)], )
        for move_line in x:
            if move_line.account_id.reconcile:
                move_line_id = move_line.id
                break;
        if self.type == 'incoming':
            action_context = {'company_ids': [self.company_id.id],
                              'partner_ids': [self.payer_user_id.commercial_partner_id.id]}
            action_context.update({'mode': 'customers'})
        else:
            action_context = {'company_ids': [self.company_id.id],
                              'partner_ids': [self.payee_user_id.commercial_partner_id.id]}
            action_context.update({'mode': 'suppliers'})
        if move_line_id:
            action_context.update({'move_line_id': move_line_id})
        print(action_context)
        return {
            'type': 'ir.actions.client',
            'tag': 'manual_reconciliation_view',
            'context': action_context,
        }

    def set_to_bounced(self):
        if self.status == 'registered':
            self.status = 'bounced'
            if self.type == 'incoming':
                x = self.payer_user_id
                date = self.cheque_receive_date
            else:
                x = self.payee_user_id
                date = self.cheque_given_date
            self.journal_items_count += 2
            self.current_state_date = datetime.today().strftime('%Y-%m-%d')
            records = []
            object1 = (
                0, 0, {
                    'name': self.name,
                    'account_id': self.debit_account_id.id,
                    'debit': 0.0,
                    'credit': self.amount,
                    'journal_id': self.journal_id.id,
                    'partner_id': x.id,
                    # 'currency_id': self.currency_id.id,
                })
            object2 = (
                0, 0, {'name': self.name,
                       'account_id': self.credit_account_id.id,
                       'debit': self.amount,
                       'credit': 0.0,
                       'journal_id': self.journal_id.id,
                       'partner_id': x.id,
                       })

            records.append(object1)
            records.append(object2)
            move_vals = {
                'ref': self.sequence + '- Bounced',
                'date': date,
                'journal_id': self.journal_id.id,
                'line_ids': records,
                'state': 'draft',
                'move_type': 'entry',
                'cheque_id': self.id

            }
            self.env['account.move'].create(move_vals)

        elif self.type == 'incoming' and self.status == 'done':
            raise ValidationError('You Cannot set bounced state in this case !')
        elif self.status == 'bank':
            date = self.cheque_return_date
            self.status = 'bounced'
            self.journal_items_count += 4
            self.current_state_date = datetime.today().strftime('%Y-%m-%d')
            records = []
            object1 = (
                0, 0, {
                    'name': self.name,
                    'account_id': self.debit_account_id.id,
                    'debit': 0.0,
                    'credit': self.amount,
                    'journal_id': self.journal_id.id,
                    'partner_id': self.payer_user_id.id,
                    # 'currency_id': self.currency_id.id,
                })
            object2 = (
                0, 0, {'name': self.name,
                       'account_id': self.credit_account_id.id,
                       'debit': self.amount,
                       'credit': 0.0,
                       'journal_id': self.journal_id.id,
                       'partner_id': self.payer_user_id.id,
                       })
            object3 = (
                0, 0, {
                    'name': self.name,
                    'account_id': self.debit_account_id.id,
                    'debit': self.amount,
                    'credit': 0.0,
                    'journal_id': self.journal_id.id,
                    'partner_id': self.payer_user_id.id,
                    # 'currency_id': self.currency_id.id,
                })
            object4 = (
                0, 0, {'name': self.name,
                       'account_id': self.cheq_under_collection_account_id.id,
                       'debit': 0.0,
                       'credit': self.amount,
                       'journal_id': self.journal_id.id,
                       'partner_id': self.payer_user_id.id,
                       })

            records.append(object1)
            records.append(object2)
            records.append(object3)
            records.append(object4)
            move_vals = {
                'ref': self.sequence + '- Bounced',
                'date': date,
                'journal_id': self.journal_id.id,
                'line_ids': records,
                'state': 'draft',
                'move_type': 'entry',
                'cheque_id': self.id
            }
            self.env['account.move'].create(move_vals)



        elif self.type == 'outgoing' and self.status == 'done':
            self.status = 'bounced'
            x = self.payee_user_id
            debit = self.credit_account_id
            credit = self.bank_account_id
            date = self.cheque_given_date
            self.journal_items_count += 4
            self.current_state_date = datetime.today().strftime('%Y-%m-%d')
            records = []
            object1 = (
                0, 0, {
                    'name': self.name,
                    'account_id': self.debit_account_id.id,
                    'debit': 0.0,
                    'credit': self.amount,
                    'journal_id': self.journal_id.id,
                    'partner_id': x.id,

                    # 'currency_id': self.currency_id.id,
                })
            object2 = (
                0, 0, {'name': self.name,
                       'account_id': self.credit_account_id.id,
                       'debit': self.amount,
                       'credit': 0.0,
                       'journal_id': self.journal_id.id,
                       'partner_id': x.id,
                       })
            object3 = (
                0, 0, {
                    'name': self.name,
                    'account_id': debit.id,
                    'debit': 0.0,
                    'credit': self.amount,
                    'journal_id': self.journal_id.id,
                    'partner_id': x.id,
                    # 'currency_id': self.currency_id.id,
                })
            object4 = (
                0, 0, {'name': self.name,
                       'account_id': credit.id,
                       'debit': self.amount,
                       'credit': 0.0,
                       'journal_id': self.journal_id.id,
                       'partner_id': x.id,
                       })

            records.append(object1)
            records.append(object2)
            records.append(object3)
            records.append(object4)

            move_vals = {
                'ref': self.sequence + '- Bounced',
                'date': date,
                'journal_id': self.journal_id.id,
                'line_ids': records,
                'state': 'posted',
                'move_type': 'entry',
                'cheque_id': self.id

            }
            self.env['account.move'].create(move_vals)

    def set_to_cancel(self):
        x = self.env['account.move'].search([('cheque_id', '=', self.id)], )
        for rec in x:
            if rec.state:
                print(rec.state)
                rec.sudo().unlink()
            else:
                raise ValidationError('This Cheque Cannot be Canceled Because of its Posted JE')
        self.status = 'draft'
        self.journal_items_count = 0
        self.current_state_date = datetime.today().strftime('%Y-%m-%d')

    # @api.one
    def incoming_action_return(self):
        x = self.env['res.config.settings'].search([], order='id desc',
                                                   limit=1)
        print(x.incoming_chq_credit_account_id.id)
        print("hsihama,a,a.a")
        tree_view_id = self.env.ref('account_cheque.incoming_cheque_tree').id
        form_view = self.env.ref('account_cheque.cheque_form_view')
        return {
            'name': ("Incoming Cheque"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.cheque',
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'tree'), (form_view.id, 'form')],
            'domain': [('type', '=', 'incoming')],
            'context': {
                'default_type': 'incoming',
                'default_credit_account_id': x.incoming_chq_credit_account_id.id,
                'default_debit_account_id': x.incoming_chq_debit_account_id.id,
                'default_journal_id':x.incoming_chq_journal.id,
                'default_cheq_under_collection_account_id': x.chq_under_coll_account_id.id,
                # cheq_under_collection_account_id

            }
        }

    # @api.one
    def outgoing_action_return(self):
        x = self.env['res.config.settings'].search([], order='id desc', limit=1)
        tree_view_id = self.env.ref('account_cheque.outgoing_cheque_tree').id
        form_view = self.env.ref('account_cheque.cheque_form_view')
        print(x.outgoing_chq_credit_account_id.id)
        print("hsihama,a,a.a")
        return {
            'name': ("Outgoing Cheque"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.cheque',
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'tree'), (form_view.id, 'form')],
            'domain': [('type', '=', 'outgoing')],
            'context': {
                'default_type': 'outgoing',
                'default_credit_account_id': x.outgoing_chq_credit_account_id.id,
                'default_debit_account_id': x.outgoing_chq_debit_account_id.id,
                'default_journal_id': x.outgoing_chq_journal.id,
                'default_cheq_under_collection_account_id': x.chq_under_coll_account_id.id,
            }
        }

    no_of_days_to_reminder = fields.Integer(string="No Of Days Before Due Date To Reminder ", default=7)

    @api.onchange('current_state_date')
    def fire_notification_1(self):
        x = self.search([('type', '=', 'incoming'), ])
        today = fields.Date.today()
        users = self.env['res.users'].search([])

        for record in x:
            m = (record.cheque_date - today).days
            print(m, record.no_of_days_to_reminder, "record.no_of_days_to_reminder")
            if m == record.no_of_days_to_reminder:
                for user in users:
                    if user.has_group('account_cheque.group_cheque_notification'):
                        record.activity_schedule('account_cheque.schdule_activity_manager_id', record.cheque_date,
                                                 user_id=user.id,
                                                 summary="Your Cheque Will be Due in %s Days !" % m)


    @api.onchange('current_state_date')
    def fire_notification_2(self):
        x = self.search([('type', '=', 'outgoing'), ])
        today = fields.Date.today()
        users = self.env['res.users'].search([])
        print("hiiiiii")

        for record in x:
            m = (record.cheque_date - today).days
            print(m,record.no_of_days_to_reminder,"record.no_of_days_to_reminder")
            if m == record.no_of_days_to_reminder:
                for user in users:
                    if user.has_group('account_cheque.group_cheque_notification'):
                        print('hiiil')
                        record.activity_schedule('account_cheque.schdule_activity_manager_id', record.cheque_date,
                                              user_id=user.id,
                                              summary="Your Cheque Will be Due in %s Days !" % m)

                print(record.create_uid.name)
                print('yalla ')


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    # My custom fields
    incoming_chq_credit_account_id = fields.Many2one(comodel_name="account.account", string="Incoming Cheque Credit Account",
                                                     required=False, )
    incoming_chq_debit_account_id = fields.Many2one(comodel_name="account.account", string="Incoming Cheque Debit Account",
                                                    required=False, )
    outgoing_chq_credit_account_id = fields.Many2one(comodel_name="account.account", string="Outgoing Cheque Credit Account",
                                                     required=False, )
    outgoing_chq_debit_account_id = fields.Many2one(comodel_name="account.account", string="Outgoing Cheque Debit Account",
                                                    required=False, )
    chq_under_coll_account_id = fields.Many2one(comodel_name="account.account",
                                                string="Cheque Under Collection Account",
                                                required=False, )
    incoming_chq_journal= fields.Many2one(comodel_name="account.journal", string="Incoming Cheque Journal",
                                                     required=False, )
    outgoing_chq_journal = fields.Many2one(comodel_name="account.journal", string="Outgoing Cheque Journal",
                                           required=False, )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        incoming_chq_credit_account_id = params.get_param('incoming_chq_credit_account_id', default=False)
        incoming_chq_debit_account_id = params.get_param('incoming_chq_debit_account_id', default=False)
        incoming_chq_journal=params.get_param('incoming_chq_journal',default=False)
        outgoing_chq_credit_account_id = params.get_param('outgoing_chq_credit_account_id', default=False)
        outgoing_chq_debit_account_id = params.get_param('outgoing_chq_debit_account_id', default=False)
        outgoing_chq_journal=params.get_param('outgoing_chq_journal',default=False)

        chq_under_coll_account_id = params.get_param('chq_under_coll_account_id', default=False)
        res.update(
            incoming_chq_credit_account_id=int(incoming_chq_credit_account_id),
            incoming_chq_debit_account_id=int(incoming_chq_debit_account_id),
            incoming_chq_journal=int(incoming_chq_journal),

            outgoing_chq_credit_account_id=int(outgoing_chq_credit_account_id),
            outgoing_chq_debit_account_id=int(outgoing_chq_debit_account_id),
            outgoing_chq_journal=int(outgoing_chq_journal),

            chq_under_coll_account_id=int(chq_under_coll_account_id),
        )
        return res

    # @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        incoming_chq_credit_account_id = self.incoming_chq_credit_account_id.id
        incoming_chq_debit_account_id = self.incoming_chq_debit_account_id.id
        incoming_chq_journal = self.incoming_chq_journal.id


        outgoing_chq_credit_account_id = self.outgoing_chq_credit_account_id.id
        outgoing_chq_debit_account_id = self.outgoing_chq_debit_account_id.id
        outgoing_chq_journal = self.outgoing_chq_journal.id
        chq_under_coll_account_id = self.chq_under_coll_account_id.id

        param.set_param('incoming_chq_credit_account_id', incoming_chq_credit_account_id)
        param.set_param('incoming_chq_debit_account_id', incoming_chq_debit_account_id)
        param.set_param('incoming_chq_journal', incoming_chq_journal)

        param.set_param('outgoing_chq_credit_account_id', outgoing_chq_credit_account_id)
        param.set_param('outgoing_chq_debit_account_id', outgoing_chq_debit_account_id)
        param.set_param('outgoing_chq_journal', outgoing_chq_journal)

        param.set_param('chq_under_coll_account_id', chq_under_coll_account_id)


class invoice_inherit(models.Model):
    _inherit = 'account.move'
    chq_id = fields.Many2one(comodel_name="account.cheque", string="", required=False, )


class journal_item_inherit(models.Model):
    _inherit = 'account.move'
    cheque_id = fields.Many2one(comodel_name="account.cheque", string="", required=False, )

class ResCurrencyInherit(models.Model):
    _inherit = 'res.currency'

    currency_unit_arabic = fields.Char(string="Arabic Currency Unit")
    currency_subunit_arabic = fields.Char(string="Arabic Currency Subunit")
