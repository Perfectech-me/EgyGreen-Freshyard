from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

class Bom(models.TransientModel):
    _name = 'cond_report_options'
    
    date_from = fields.Date(required = True)
    date_to = fields.Date(required = True)
    def get_bank_cash(self):
        journals = self.env['account.journal'].search([('type','in',['bank','cash'])])
        datas = []
        for journal in journals:
            data = {
                'name' : journal.name,
                'balance_currency' : 0,
                'balance_egp' : 0,
            }
            amls = self.env['account.move.line'].search([('move_id.state','=','posted'),('account_id','=',journal.default_account_id.id),('date','>=',self.date_from),('date','<=',self.date_to)])
            if not amls:
                continue
            for aml in amls:
                data['balance_currency'] += aml.amount_currency
                data['balance_egp'] += aml.balance
            datas.append(data)
                
    def get_cheque(self):
        pass
    def get_invoices(self):
        pass
    def get_bills(self):
        pass
    def print(self):
        return self.env.ref('gogs_and_condition_report.cond_xlsx').report_action(self.env['account.move'], data={
            'bank_cash' : self.get_bank_cash(),
            'cheques' : self.get_cheque(),
            'invoices' : self.get_invoices(),
            'bills' : self.get_bills(),
        })






