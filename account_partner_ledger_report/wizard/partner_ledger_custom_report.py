from odoo import models, fields, api

class PartnerReportLedgerCustom(models.TransientModel):
    _name = 'partner.report.ledger.custom'
    _description = 'Partner Ledger Report Custom'


    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    partner_ids = fields.Many2many(comodel_name="res.partner", string="Partner")
    analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Analytic Tags")
    account_type = fields.Selection(string="Account Type", selection=[('receivable', 'Receivable'), ('payable', 'Payable'), ])
    currency_ids = fields.Many2many(comodel_name="res.currency",string="Currency")
    analytic_account_ids = fields.Many2many(comodel_name="account.analytic.account",string="Analytic Account")


    def button_print(self):
        return self.env.ref('account_partner_ledger_report.partner_ledger_report_xlsx').report_action(self)

    def button_print_pdf(self):

        data = {}
        wizard_data = []
        account_type = [self.env.ref('account.data_account_type_receivable').id,
                        self.env.ref('account.data_account_type_payable').id]

        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to),('move_id.state','=','posted')]


        partner_name = []
        analytic_tags = []
        currency_list = []
        analytic_accounts = []

        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))

            for par in self.env['res.partner'].search([('id','in',self.partner_ids.ids)]):
                partner_name.append(par.name)

        if self.analytic_tag_ids:
            domain.append(('analytic_tag_ids', 'in', self.analytic_tag_ids.ids))

            for par in self.env['account.analytic.tag'].search([('id', 'in', self.analytic_tag_ids.ids)]):
                analytic_tags.append(par.name)

        if self.currency_ids:
            domain.append(('currency_id', 'in', self.currency_ids.ids))

            for par in self.env['res.currency'].search([('id', 'in', self.currency_ids.ids)]):
                currency_list.append(par.name)


        if self.analytic_account_ids:
            domain.append(('analytic_account_id', 'in', self.analytic_account_ids.ids))

            for par in self.env['account.analytic.account'].search([('id', 'in', self.analytic_account_ids.ids)]):
                analytic_accounts.append(par.name)


        if self.account_type=='receivable':
            domain.append(('account_id.user_type_id.id', '=', self.env.ref('account.data_account_type_receivable').id))
        elif self.account_type=='payable':
            domain.append(('account_id.user_type_id.id', '=', self.env.ref('account.data_account_type_payable').id))

        else:
            domain.append(('account_id.user_type_id.id', 'in', account_type))


        account_move_line_record = self.env['account.move.line'].search(domain,order='id asc')

        total_debit = 0.0
        total_credit = 0.0
        account_move_lines=[]
        partner_list=[]

        for par in account_move_line_record:
            partner_list.append(par.partner_id.id)

        if account_move_line_record:


            for part in self.env['res.partner'].search([('id','in',partner_list)]):
                balance = 0.0
                initial_balance = 0.0
                counter = 0
                for line in account_move_line_record:
                    if part.id == line.partner_id.id:
                        credit=0
                        debit=0
                        if line.debit:
                            debit=line.amount_currency if line.amount_currency>0 else line.amount_currency*-1
                        elif line.credit:
                            credit=line.amount_currency if line.amount_currency>0 else line.amount_currency*-1

                        account_move_line_initial_balance = self.env['account.move.line'].search(
                            [('date', '<', self.date_from),('partner_id','=',line.partner_id.id),('date_maturity','!=',False)],order='date_maturity asc')

                        if account_move_line_initial_balance and counter==0:

                            if self.account_type=='receivable' and account_move_line_initial_balance.account_id.user_type_id.id==self.env.ref('account.data_account_type_receivable').id:
                                initial_balance=account_move_line_initial_balance.balance

                            elif self.account_type == 'payable' and account_move_line_initial_balance.account_id.user_type_id.id == self.env.ref(
                                    'account.data_account_type_payable').id:
                                initial_balance = account_move_line_initial_balance.balance

                            elif self.account_type==False and account_move_line_initial_balance.account_id.user_type_id.id in account_type:
                                initial_balance = account_move_line_initial_balance.balance



                        if debit>0 and credit<debit:

                            balance=debit+initial_balance
                        else:
                            balance=credit-initial_balance
                            if balance<0:
                                balance=balance*-1

                        account_move_lines.append({
                        'partner': line.partner_id.name or "",
                        'journal_id': line.journal_id.name or "",
                        'account_id': line.account_id.name or "",
                        'desc': line.name or "",
                        'ref': line.ref or "",
                        'date_maturity': line.date_maturity or "",
                        'matching_number': line.matching_number or "",
                        'initial_balance':  initial_balance or 0,
                        "debit": debit,
                        "credit": credit,
                        "amount_currency": line.amount_currency or 0,
                        "balance": balance or 0,
                         "currency_id":line.currency_id.symbol,
                        })
                        initial_balance=balance
                        counter+=1


        wizard_data.append({
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_name': partner_name,
            'analytic_tags': analytic_tags,
            'account_type': self.account_type,
            'currency_list': currency_list,
            'analytic_accounts': analytic_accounts,
        })

        data['wizard_data'] = wizard_data
        data['account_move_lines'] = account_move_lines

        return self.env.ref('account_partner_ledger_report.partners_ledger_report_pdf').report_action(self,data=data)



class PartnerLedgerReportPDF(models.AbstractModel):
    _name = 'report.account_partner_ledger_report.pdf_partner'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('account_partner_ledger_report.pdf_partner')
        wizard_data = data.get('wizard_data')
        account_move_lines=data.get('account_move_lines')
        return {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'wizard_data': wizard_data,
            'account_move_lines':account_move_lines,
        }
