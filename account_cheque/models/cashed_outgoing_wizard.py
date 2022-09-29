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
        object1 = (
            0, 0, {
                'name': self.cheque_id.name,
                'account_id': debit.id,
                'debit': self.cheque_id.amount,
                'credit': 0.0,
                'journal_id': self.cheque_id.journal_id.id,
                'partner_id': x.id,
                # 'currency_id': self.currency_id.id,
            })
        object2 = (
            0, 0, {'name': self.cheque_id.name,
                   'account_id': credit.id,
                   'debit': 0.0,
                   'credit': self.cheque_id.amount,
                   'journal_id': self.cheque_id.journal_id.id,
                   'partner_id': x.id,
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
        self.env['account.move'].create(move_vals)
