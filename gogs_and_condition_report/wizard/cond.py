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
        return datas
    def get_cheque(self):
        cheques = self.env['account.cheque'].search([('type', '=', 'outgoing'),('status','not in',['draft','done'])])
        datas = []
        for cheque in cheques:
            
            datas.append({
                'date' : cheque.cheque_date,
                'amount_currency' : cheque.amount,
                'amount_egp' : cheque.amount_egy,
                'cheque_number' : cheque.chq_no,
                'bank_account' : cheque.bank_account_id.name,
                'payee' : cheque.payee_user_id.name,
            })
        return datas
    def get_invoices(self):
        invoices = self.env['account.move'].search([('state','=','posted'),('move_type','=','out_invoice'),('invoice_date','>=',self.date_from),('invoice_date','<=',self.date_to)])
        datas = []
        for invoice in invoices:
            credit_note = self.env['account.move'].search([('reversed_entry_id','=',invoice.id),('state','=','posted')])
            credit_ratio = abs(sum(credit_note.mapped('amount_total_signed')))
            if not invoice.amount_residual_signed:
                continue
            datas.append({
                'due_date' : invoice.invoice_date_due,
                'amount_currency' : invoice.amount_residual,
                'amount_egp' : invoice.amount_residual_signed,
                'credit_ratio' : credit_ratio ,
                'net_amount' : invoice.amount_residual_signed - credit_ratio,
                'invoice' : invoice.name,
                'date' : invoice.invoice_date,
                
                'customer' : invoice.partner_id.name,
                'payment_term' : invoice.partner_id.property_payment_term_id.name,
                'salesperson' : invoice.invoice_person_user_id.name,
            })
        return datas
    def get_bills(self):
        invoices = self.env['account.move'].search([('state','=','posted'),('move_type','=','in_invoice'),('invoice_date','>=',self.date_from),('invoice_date','<=',self.date_to)])
        datas = []
        for invoice in invoices:
            if not invoice.amount_residual_signed:
                continue
            datas.append({
                'due_date' : invoice.invoice_date_due,
                'amount_currency' : abs(invoice.amount_residual),
                'amount_egp' : abs(invoice.amount_residual_signed),
                'invoice' : invoice.name,
                'date' : invoice.invoice_date,
                'customer' : invoice.partner_id.name,
                'payment_term' : invoice.partner_id.property_payment_term_id.name,
            })
        return datas
    def print(self):
        return self.env.ref('gogs_and_condition_report.cond_xlsx').report_action(self.env['account.move'], data={
            'bank_cash' : self.get_bank_cash(),
            'cheques' : self.get_cheque(),
            'invoices' : self.get_invoices(),
            'bills' : self.get_bills(),
            'date_from' : self.date_from,
            'date_to' : self.date_to,
            
        })






