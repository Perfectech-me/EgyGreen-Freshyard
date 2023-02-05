from odoo import models, fields, api
class cashedWizard(models.TransientModel):
    _name='cashed.wizard'
    _description = 'Cashed Wizard'

    cheque_id = fields.Many2one(comodel_name="account.cheque", string="", required=False, )
    date = fields.Date(string="Cheque Date", required=False, )
    bank_account_id = fields.Many2one(comodel_name="account.account", string="Bank Account", required=False,domain=[('name','ilike', 'bank')] )
    def cashed_wizard(self):
        self.cheque_id.status='done'
        x = self.cheque_id.payee_user_id
        debit = self.cheque_id.credit_account_id
        credit = self.bank_account_id
        self.cheque_id.journal_items_count += 2
        records = []

        rate = 0
        debit_amount = 0
        credit_amount = 0
        if self.cheque_id.currency_id.id == self.cheque_id.company_id.currency_id.id:
            debit_amount = self.cheque_id.amount
            credit_amount = self.cheque_id.amount
        else:

            rates_current = []
            if self.cheque_id.currency_id:
                rates = self.cheque_id.currency_id.rate_ids.mapped('name')
                for line in rates:
                    if line <= self.date:
                        rates_current.append(line)
                for line in self.cheque_id.currency_id.rate_ids:
                    if rates_current and max(set(rates_current)) == line.name:
                        rate = line.inverse_company_rate

            if rate > 0:
                credit_amount = debit_amount = self.cheque_id.amount * rate
            else:
                debit_amount = 0
                credit_amount = 0

        object1 = (
            0, 0, {
                'name': self.cheque_id.name,
                'account_id': debit.id,
                'amount_currency': self.cheque_id.amount,
                'debit': debit_amount,
                'credit': 0.0,
                'journal_id': self.cheque_id.journal_id.id,
                'partner_id': x.id,
                'currency_id': self.cheque_id.currency_id.id,
            })
        object2 = (
            0, 0, {'name': self.cheque_id.name,
                   'account_id': credit.id,
                   'debit': 0.0,
                   'amount_currency': -self.cheque_id.amount,
                   'credit': credit_amount,
                   'journal_id': self.cheque_id.journal_id.id,
                   'partner_id': x.id,
                   'currency_id': self.cheque_id.currency_id.id,

                   })

        records.append(object1)
        records.append(object2)
        move_vals = {
            'ref': self.cheque_id.sequence + '- Cashed',
            'date': self.date,
            'journal_id': self.cheque_id.journal_id.id,
            'line_ids': records,
            'state': 'draft',
            'cheque_id': self.cheque_id.id
        }
        account_move=self.env['account.move'].create(move_vals)
        if account_move and account_move.line_ids:
            for line in account_move.line_ids:
                line.get_currency_rate()