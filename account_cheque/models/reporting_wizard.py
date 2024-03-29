from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import timedelta, datetime

import pandas as pd
# import datetime
import time
from dateutil.rrule import rrule, MONTHLY

class account_move_report_wizard(models.Model):
    _name = 'cheque.wizard'
    _description = 'Cheque Wizard'

    payer_user_id = fields.Many2one(comodel_name="res.partner", string="Payer", required=False, )
    payee_user_id = fields.Many2one(comodel_name="res.partner", string="Payee", required=False, )
    from_date = fields.Date(string="From", required=True, )
    to_date = fields.Date(string="To", required=True, )


    status = fields.Selection(string="",
                              selection=[('draft', 'Draft'), ('registered', 'Registered'), ('bank', 'Bank Repository'),
                                         ('bounced', 'Bounced'),
                                         ('done', 'Done'), ('cancel', 'Cancel'), ], required=False)
    type = fields.Selection(string="", selection=[('incoming', 'incoming'), ('outgoing', 'outgoing'), ],
                            required=True )

    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account")
    bank_account_id = fields.Many2one(comodel_name="account.account", string="Bank Account")
    account_type_ids = fields.Many2many(comodel_name="account.account.type", string="نوع الحساب" ,compute='compute_account_type')
    date_type = fields.Selection(string="", selection=[('cheque_date', 'Cheque Date'), ('cheque_given_date', 'Cheque Given Date')],default='cheque_date')


    @api.depends('from_date', 'to_date')
    def compute_account_type(self):
        for rec in self:
            rec.account_type_ids = False
            lines = []
            lines.append(self.env.ref('account.data_account_type_liquidity').id)
            rec.account_type_ids = lines

    # @api.multi
    def get_today(self):
        return datetime.today().date()
    # @api.multi
    def if_status(self):
        if self.status:
            return True

    # @api.multi
    def generate_cheque_report(self):
        domain=[]
        # month_list=[]
        date1=datetime.strptime(str(self.from_date), "%Y-%m-%d").date()
        date2=datetime.strptime(str(self.to_date), "%Y-%m-%d").date()

        # for i in pd.date_range(start=date1, end=date2, freq='MS'):
        #     print(i,"EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        #     month_list.append(i.strftime("%b-%y"))
        #     print("11111111111111111111111111111111",i.strftime("%b-%y"))
        # month_list = [i.strftime("%b-%y") for i in pd.date_range(start=date1, end=date2, freq='MS')]
        #
        # print(month_list,"************************************************")

        delta = date2 - date1  # returns timedelta
        month_list=[]
        for i in range(delta.days + 1):
            day = date1 + timedelta(days=i)
            if day.month not in month_list:
                month_list.append(day.strftime("%b-%y"))

        print(set(month_list),"TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTt")


        if self.date_type=='cheque_date':
            domain.append (('cheque_date', '>=', self.from_date))
            domain.append(('cheque_date', '<=', self.to_date))

        elif self.date_type=='cheque_given_date':
            domain.append(('cheque_given_date', '>=', self.from_date))
            domain.append(('cheque_given_date', '<=', self.to_date))

        if self.payer_user_id:
            domain.append(('payer_user_id', '=', self.payer_user_id.id))
        if self.status:
            domain.append(('status', '=', self.status))
        if self.payee_user_id:
            domain.append(('payee_user_id', '=', self.payee_user_id.id))

        if self.analytic_account_id:
            domain.append(('analytic_account_id', '=', self.analytic_account_id.id))

        if self.analytic_account_id:
            domain.append(('analytic_account_id', '=', self.analytic_account_id.id))

        if self.bank_account_id:
            domain.append(('bank_account_id', '=', self.bank_account_id.id))
        domain.append(('type', '=', self.type))

        total_month_amount=[]
        for month in set(month_list):
            total_amount=0.0
            for cheque in self.env['account.cheque'].search(domain):
                if self.date_type=='cheque_date':
                    cheque_date=datetime.strptime(str(cheque.cheque_date), "%Y-%m-%d").date()
                    if month==cheque_date.strftime("%b-%y"):
                        total_amount+=cheque.amount_egy
                elif self.date_type == 'cheque_given_date':
                    cheque_date = datetime.strptime(str(cheque.cheque_given_date), "%Y-%m-%d").date()
                    if month == cheque_date.strftime("%b-%y"):
                        total_amount += cheque.amount_egy

            if total_amount>0:
                total_month_amount.append({
                    'month':month,
                    'total_amount':total_amount,
                })


        if self.type=='incoming':
            return self.env['account.cheque'].search(domain)
        else:
            return [self.env['account.cheque'].search(domain),total_month_amount]

    # @api.multi
    def incoming_report_method(self):
        return self.env.ref('account_cheque.incoming_report_get').report_action(self)

    # @api.multi
    def outgoing_report_method(self):

        if self.from_date > self.to_date :
            raise ValidationError('تاريخ البدأ أكبر من تاريخ النتهاء')


        return self.env.ref('account_cheque.outgoing_report_get').report_action(self)

    def outgoing_print_method(self):
        return self.env.ref('account_cheque.print_get').report_action(self)

