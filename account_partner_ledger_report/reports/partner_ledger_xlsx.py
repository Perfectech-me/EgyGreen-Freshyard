from odoo import models, fields, api
from odoo import models
import datetime
from datetime import date, datetime, time, timedelta
from pytz import timezone
import xlsxwriter

from odoo.exceptions import ValidationError
class PartnerLedgerReportXlsx(models.AbstractModel):
    _name = 'report.account_partner_ledger_report.print_partner_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#237aab', 'color': 'white'})

        header_format_lines = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter'})

        header_format_lines_left = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter'})

        format_total_lines = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter','bg_color': '#237aab','color': 'white'})

        worksheet = workbook.add_worksheet('Journal Entries')

        worksheet.set_column('A:A', 18)
        worksheet.set_column('B:B', 18)
        worksheet.set_column('C:C', 18)
        worksheet.set_column('D:D', 18)
        worksheet.set_column('E:E', 18)
        worksheet.set_column('G:G', 18)
        worksheet.set_column('F:F', 18)
        worksheet.set_column('H:H', 18)
        worksheet.set_column('I:I', 18)
        worksheet.set_column('J:J', 18)
        worksheet.set_column('K:K', 18)
        worksheet.set_column('L:L', 18)


        worksheet.merge_range('A1:H1',  "Partner Ledger Report", header_format)

        worksheet.write('B3', 'Date From', header_format)
        worksheet.write('C3', str(partners.date_from) , header_format_lines)

        worksheet.write('D3', 'Date To', header_format)
        worksheet.write('E3', str(partners.date_to), header_format_lines)

        worksheet.write('F3', 'Account Type', header_format)

        if partners.account_type=='receivable':
            worksheet.write('G3', "Receivable", header_format_lines)
        elif partners.account_type=='payable':
            worksheet.write('G3', "Payable", header_format_lines)
        else:
            worksheet.write('G3', " ", header_format_lines)


        worksheet.write('B4', 'Partners', header_format)
        worksheet.merge_range('C4:G4',  "", header_format_lines)

        if partners.partner_ids:
            partner_name=""
            for partner in self.env['res.partner'].search([('id','in',partners.partner_ids.ids)]):
                partner_name+=partner.name + " , "
            worksheet.write('C4', partner_name, header_format_lines_left)

        worksheet.write('B5', 'Analytic Tags', header_format)
        worksheet.merge_range('C5:G5', "", header_format_lines)

        if partners.analytic_tag_ids:
            analytic_name = ""
            for analytic in self.env['account.analytic.tag'].search([('id', 'in', partners.analytic_tag_ids.ids)]):
                analytic_name += analytic.name + " , "
            worksheet.write('C5', analytic_name, header_format_lines_left)

        worksheet.write('B6', 'Analytic Account', header_format)
        worksheet.merge_range('C6:G6', "", header_format_lines)

        if partners.analytic_account_ids:
            analytic_name = ""
            for analytic in self.env['account.analytic.account'].search([('id', 'in', partners.analytic_account_ids.ids)]):
                analytic_name += analytic.name + " , "
            worksheet.write('C6', analytic_name, header_format_lines_left)

        worksheet.write('B7', 'Currency', header_format)
        worksheet.merge_range('C7:G7', "", header_format_lines)

        if partners.currency_ids:
            currency_name = ""
            for currency in self.env['res.currency'].search(
                    [('id', 'in', partners.currency_ids.ids)]):
                currency_name += currency.symbol + " , "
            worksheet.write('C7', currency_name, header_format_lines_left)

        worksheet.write('A10', 'Date', header_format)
        worksheet.write('B10', 'Journal', header_format)
        worksheet.write('C10', 'Account', header_format)
        worksheet.write('D10', 'Desc', header_format)
        worksheet.write('E10', 'Ref', header_format)
        worksheet.write('F10', ' Due Date ', header_format)
        worksheet.write('G10', '  Matching Number', header_format)
        worksheet.write('H10', 'Debit', header_format)
        worksheet.write('I10', 'Credit', header_format)
        worksheet.write('J10', ' Balance', header_format)

        account_type = [self.env.ref('account.data_account_type_receivable').id,
                        self.env.ref('account.data_account_type_payable').id]

        domain = [('date', '>=', partners.date_from), ('date', '<=', partners.date_to), ('move_id.state', '=', 'posted')]

        partner_name = []
        analytic_tags = []
        currency_list = []
        analytic_accounts = []

        if partners.partner_ids:
            domain.append(('partner_id', 'in', partners.partner_ids.ids))

            for par in self.env['res.partner'].search([('id', 'in', partners.partner_ids.ids)]):
                partner_name.append(par.name)

        if partners.analytic_tag_ids:
            domain.append(('analytic_tag_ids', 'in', partners.analytic_tag_ids.ids))

            for par in self.env['account.analytic.tag'].search([('id', 'in', partners.analytic_tag_ids.ids)]):
                analytic_tags.append(par.name)

        if partners.currency_ids:
            domain.append(('currency_id', 'in', partners.currency_ids.ids))

            for par in self.env['res.currency'].search([('id', 'in', partners.currency_ids.ids)]):
                currency_list.append(par.name)

        if partners.analytic_account_ids:
            domain.append(('analytic_account_id', 'in', partners.analytic_account_ids.ids))

            for par in self.env['account.analytic.account'].search([('id', 'in', partners.analytic_account_ids.ids)]):
                analytic_accounts.append(par.name)

        if partners.account_type == 'receivable':
            domain.append(('account_id.user_type_id.id', '=', self.env.ref('account.data_account_type_receivable').id))
        elif partners.account_type == 'payable':
            domain.append(('account_id.user_type_id.id', '=', self.env.ref('account.data_account_type_payable').id))

        else:
            domain.append(('account_id.user_type_id.id', 'in', account_type))

        account_move_line_record = self.env['account.move.line'].search(domain, order='date asc')

        number = 1
        row = 10
        col = 0
        account_move_lines = []
        partner_list = []
        if account_move_line_record:
            for par in account_move_line_record:
                partner_list.append(par.partner_id.id)

            for part in self.env['res.partner'].search([('id', 'in', partner_list)]):
                balance = 0.0
                initial_balance = 0.0
                count = 0
                for line in account_move_line_record:
                    if part.id == line.partner_id.id:
                        credit = 0
                        debit = 0
                        if line.debit:
                            debit = line.amount_currency if line.amount_currency > 0 else line.amount_currency * -1
                        elif line.credit:
                            credit = line.amount_currency if line.amount_currency > 0 else line.amount_currency * -1
                        domain_init = [('date', '<', partners.date_from),('partner_id','=',line.partner_id.id),('move_id.state','=','posted')]
                        if partners.analytic_tag_ids:
                            domain_init.append(('analytic_tag_ids', 'in', partners.analytic_tag_ids.ids))
                
                
                        if partners.currency_ids:
                            domain_init.append(('currency_id', 'in', partners.currency_ids.ids))
                
                        if partners.analytic_account_ids:
                            domain_init.append(('analytic_account_id', 'in', partners.analytic_account_ids.ids))
                
                
                        if partners.account_type == 'receivable':
                            domain_init.append(('account_id.user_type_id.id', '=', self.env.ref('account.data_account_type_receivable').id))
                        elif partners.account_type == 'payable':
                            domain_init.append(('account_id.user_type_id.id', '=', self.env.ref('account.data_account_type_payable').id))
                
                        else:
                            domain_init.append(('account_id.user_type_id.id', 'in', account_type))
                        account_move_line_initial_balance = self.env['account.move.line'].search(
                            domain_init,order = "date")

                        if account_move_line_initial_balance and count == 0:
                            initial_balance = sum([l.amount_currency for l in account_move_line_initial_balance])                            
                        if debit > 0 and credit == 0:
                            balance = debit + initial_balance
                        elif credit > 0 and debit == 0:
                            balance = initial_balance - credit

                        account_move_lines.append({
                            'partner': line.partner_id.name or "",
                            'journal_id': line.journal_id.name or "",
                            'account_id': line.account_id.name or "",
                            'desc': line.name or "",
                            'ref': line.ref or "",
                            'date_maturity': line.date_maturity or "",
                            'matching_number': line.get_matching_number() or "",
                            'initial_balance': initial_balance or 0,
                            "debit": debit,
                            "credit": credit,
                            "date" : line.date,
                            "amount_currency": line.amount_currency or 0,
                            "balance": balance or 0,
                            "currency_id": line.currency_id.symbol,
                        })
                        initial_balance = balance
                        count += 1
            for lines in account_move_lines:
                    worksheet.write(row, col, str(lines['date']), header_format_lines)
                    worksheet.write(row, col + 1, str(lines['journal_id']), header_format_lines)
                    worksheet.write(row, col + 2, str(lines['account_id']), header_format_lines)
                    worksheet.write(row, col + 3, str(lines['desc']), header_format_lines)
                    worksheet.write(row, col + 4, str(lines['ref']), header_format_lines)
                    worksheet.write(row, col + 5, str(lines['date_maturity']), header_format_lines)
                    worksheet.write(row, col + 6, str(lines['matching_number']), header_format_lines)
                    worksheet.write(row, col + 7, str("{:,.2f}".format(lines['debit'])) +" "+ str(lines['currency_id']), header_format_lines)
                    worksheet.write(row, col + 8, str("{:,.2f}".format(lines['credit'])) +" "+ str(lines['currency_id']), header_format_lines)
                    worksheet.write(row, col + 9, str("{:,.2f}".format(lines['balance'])) +" "+ str(lines['currency_id']), header_format_lines)
                    number += 1
                    row += 1