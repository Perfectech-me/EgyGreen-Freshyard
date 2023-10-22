from odoo import models
from odoo.exceptions import ValidationError
import datetime
class PartnerXlsx(models.AbstractModel):
    _name = 'report.cond_xlsx'
    _inherit = 'report.report_xlsx.partner_xlsx'
    
    def get_formats_dict(self,workbook):
        formats = {}
        border = 2
        heading_font_size = 8
        sub_heading_font_size = 10
        normal_font_size = 11
        heading_base_format = {
            'border':border,
            'bold':True,
            'font_size':heading_font_size,
            'align':'vcenter',
        }
        heading_base_format_blue = {
            'border':border,
            'bold':True,
            'font_size':heading_font_size,
            'align':'vcenter',
            'bg_color' : '#1f497d',
            'font_color' : 'white',
            
        }
        formats['normal'] = workbook.add_format(heading_base_format)
        formats['normal_blue'] = workbook.add_format(heading_base_format_blue)        
        formats['normal'].set_align('center')
        formats['normal'].set_text_wrap()
        formats['normal_blue'].set_align('center')
        formats['normal_blue'].set_text_wrap()
        return formats

    def write_line(self,sheet,formats,cells,row_start,format_name = 'normal',cell_start = 0):
        for cell in cells:
            sheet.set_column(cell_start, cell_start, 20)

            sheet.write(row_start,cell_start,cell,formats[format_name])
            cell_start += 1


    def write_cash(self,sheet,formats,data,row_start):
        headers = ["Bank and Cash item", "Balance Currency", "Balance EGP","Current Balance","Current Balance Currency"]
        sheet.merge_range(row_start, 0, row_start, len(headers) - 1, 'Bank and Cash Conditions', formats['normal'])
        row_start += 1
        self.write_line(sheet,formats,headers,row_start)
        row_start += 1
        totals = ['Totals',0,0]
        for rec in data:
            self.write_line(sheet,formats,rec.values(),row_start)
            totals[1] += list(rec.values())[1]
            totals[2] += list(rec.values())[2]
            
            row_start += 1
        self.write_line(sheet,formats,totals,row_start)
        row_start += 1
        return row_start
        
    def write_cheque(self,sheet,formats,data,row_start):
        headers = ["Cheque Date", "Amount Currency", "Amount EGP", "Cheque Number", "Bank Account", "Payee"]
        sheet.merge_range(row_start, 0, row_start, len(headers) - 1, 'Cheques Conditions', formats['normal_blue'])
        row_start += 1
        self.write_line(sheet,formats,headers,row_start,'normal_blue')
        row_start += 1
        totals = ['totals',0,0,'','','']
        for rec in data:
            self.write_line(sheet,formats,rec.values(),row_start)
            totals[1] += list(rec.values())[1]
            totals[2] += list(rec.values())[2]
            row_start += 1
        self.write_line(sheet,formats,totals,row_start)
        row_start += 1
        return row_start
    def write_invoice(self,sheet,formats,data,row_start):
        headers = [
            "Due Date",
            "Amount Currency",
            "Amount EGP",
            "Credit Ratio",
            "Net Amount",
            "Customer Invoice",
            "Invoice Date",
            "Customer",
            "Payment Term",
            "Sales Person"
        ]
        sheet.merge_range(row_start, 0, row_start, len(headers) - 1, 'Customers Conditions', formats['normal_blue'])
        row_start += 1
        self.write_line(sheet,formats,headers,row_start,'normal_blue')
        row_start += 1
        totals = ['totals',0,0,'','','','','','','']
        for rec in data:
            self.write_line(sheet,formats,rec.values(),row_start)
            totals[1] += list(rec.values())[1]
            totals[2] += list(rec.values())[2]
            row_start += 1
        self.write_line(sheet,formats,totals,row_start)
        row_start += 1
        return row_start
    def write_bill(self,sheet,formats,data,row_start):
        headers = ["Due Date", "Amount Currency", "Amount EGP", "Bill Reffrence", "Bill Date", "Vendor", "Payment Term"]

        sheet.merge_range(row_start, 0, row_start, len(headers) - 1, 'Vendors Conditions', formats['normal_blue'])
        row_start += 1
        self.write_line(sheet,formats,headers,row_start,'normal_blue')
        row_start += 1
        totals = ['totals',0,0,'','','','']
        for rec in data:
            self.write_line(sheet,formats,rec.values(),row_start)
            totals[1] += list(rec.values())[1]
            totals[2] += list(rec.values())[2]
            row_start += 1
        self.write_line(sheet,formats,totals,row_start)
        row_start += 1
        return row_start

    def write_totals(self,sheet,formats,data,row_start):
        total_invoice = sum([i['amount_egp'] for i in data['invoices']])
        total_bill = sum([i['amount_egp'] for i in data['bills']])
        total_cheque = sum([i['amount_egp'] for i in data['cheques']])
        total_cash = sum([i['balance_egp'] for i in data['bank_cash']])
        self.write_line(sheet,formats,[f"date from : {data['date_from']}",f"date to : {data['date_to']}"],row_start,'normal_blue')
        row_start += 1
        self.write_line(sheet,formats,['Total Reciveable / EGP'],row_start,'normal_blue')
        self.write_line(sheet,formats,[total_invoice],row_start,'normal',1)
        row_start += 1
        
        self.write_line(sheet,formats,['Bank and Cash Conditions'],row_start,'normal_blue')
        self.write_line(sheet,formats,[total_cash],row_start,'normal',1)
        row_start += 1
        
        self.write_line(sheet,formats,['Total Payable / EGP'],row_start,'normal_blue')
        self.write_line(sheet,formats,[total_cheque + total_bill],row_start,'normal',1)
        row_start += 1
        
        self.write_line(sheet,formats,['Financial Condition'],row_start,'normal_blue')
        self.write_line(sheet,formats,[total_invoice + total_cash  - total_cheque - total_bill],row_start,'normal',1)
        
        
        
        
        
        
        
        
    def generate_xlsx_report(self, workbook, data, recs):
        sheet_1 = workbook.add_worksheet("Report")
        formats = self.get_formats_dict(workbook)
        sheet_1.merge_range(0, 0, 0, 6, 'Financial Condition Report', formats['normal_blue'])
        self.write_line(sheet_1,formats,[f"date from : {data['date_from']}",'','','',f"date to : {data['date_to']}"],1,'normal_blue')
        row_start = self.write_cash(sheet_1,formats,data['bank_cash'],2)
        row_start = self.write_cheque(sheet_1,formats,data['cheques'],row_start)
        row_start = self.write_bill(sheet_1,formats,data['bills'],row_start)
        row_start = self.write_invoice(sheet_1,formats,data['invoices'],row_start)
        row_start = self.write_totals(sheet_1,formats,data,row_start)
        
        
        