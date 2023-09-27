from odoo import models
from odoo.exceptions import ValidationError
import datetime
class PartnerXlsx(models.AbstractModel):
    _name = 'report.gogs_xlsx'
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
    def set_headers(self,sheet,formats):

        header_cells = [
                    "Analytic Tags",
                    "Analytic Account",
                    "Customer Invoice",
                    "Invoice Date",
                    "Customer",
                    "Sales employee",
                    "Container/Equipment Number",
                    "Total Net Weight / KG",
                    "Total Product or BOM Cost",
                    "Shipping Type",
                    "Total Services Cost",
                    "Landed Cost",
                    "Grand Total Cost",
                    "Total Amount Currency",
                    "Total Amount EGP",
                    "Credit Note Amount Currency",
                    "Credit Note Amount EGP",
                    "Net Profit/Loss",
                    "Percentage Profit/Loss",
                    "Invoice Amount Due",
                    "Payment Terms"
            ]
        self.write_line(sheet,formats,header_cells,1,'normal_blue')
    def get_analyc_tags_cost(self,rec):
        tags = []
        cost = 0
        for line in rec.invoice_line_ids:
            for tag in line.analytic_tag_ids:
                tags.append(tag.id)
        for tag in tags:
            bill_lines = self.env['account.move.line'].search([('analytic_tag_ids','in',[tag]),('move_id.state','=','posted'),('move_id.move_type','=','in_invoice')])
            cost += abs(sum(bill_lines.mapped('move_id.amount_total_signed')))
        return cost
    def get_analytic_tags(self,rec):
        tags = []
        for line in rec.invoice_line_ids:
            for tag in line.analytic_tag_ids:
                tags.append(tag.name or '')
        return ','.join(list(set(tags)))
    def get_analytic_account(self,rec):
        tags = []
        for line in rec.invoice_line_ids:
            tags.append(line.analytic_account_id.name or '')
        return ','.join(list(set(tags)))
    def get_sale_order(self,rec):
        order = self.env['sale.order'].search([('invoice_ids','in',[rec.id])],limit = 1)
        return order
    def get_landed_cost(self,sale):
        procurement_groups = self.env['procurement.group'].search([('sale_id', 'in', sale.ids)])
        mrp_production_ids = set(procurement_groups.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids) |\
            set(procurement_groups.mrp_production_ids)
        landed_cost = 0
        for m in mrp_production_ids:
            landed_costs = self.env['stock.landed.cost'].search([('mrp_production_ids','in',[m.id])])
            for landed in landed_costs:
                landed_cost += landed.amount_total
        return landed_cost
    def get_credit_notes(self,rec):
        return self.env['account.move'].search([('reversed_entry_id','=',rec.id),('state','=','posted')])
    def write_lines(self,sheet,formats,recs):
        self.set_headers(sheet,formats)
        row_start = 2
        i = 1
        for rec in recs:
            credit_notes = self.get_credit_notes(rec)
            so = self.get_sale_order(rec)
            net_weight = sum(line.net_weight_per_unit * line.product_uom_qty for line in so.order_line or [])
            total_cost = sum(line.product_id.standard_price for line in rec.invoice_line_ids)
            shipping_type = so.shipping_line_type or ''
            total_service_cost = self.get_analyc_tags_cost(rec)
            landed_cost = self.get_landed_cost(so)
            credit_note_amount_in_currency = abs(sum(credit_notes.mapped('amount_total_in_currency_signed')))
            credit_note_amount_egp = abs(sum(credit_notes.mapped('amount_total_signed')))
            grand_total_cost = total_cost + total_service_cost + landed_cost
            cells = [self.get_analytic_tags(rec),
                     self.get_analytic_account(rec),
                     rec.name,
                     rec.invoice_date.strftime('%d-%m-%Y'),
                     rec.partner_id.name,
                     rec.invoice_person_user_id.name,
                     rec.container_equipment_number,
                     net_weight,
                     total_cost,
                     shipping_type,
                     total_service_cost,
                     landed_cost,
                     grand_total_cost,
                     rec.amount_total_in_currency_signed,
                     rec.amount_total_signed,
                     credit_note_amount_in_currency,
                     credit_note_amount_egp,
                     rec.amount_total_signed - credit_note_amount_egp - grand_total_cost,
                     ((rec.amount_total_signed - credit_note_amount_egp - grand_total_cost) / rec.amount_total_signed if rec.amount_total_signed else 0) * 100,
                     rec.amount_residual,
                     so.payment_term_id.name 
                    ]
            self.write_line(sheet,formats,cells,row_start)
            row_start += 1
            i += 1
    def write_line(self,sheet,formats,cells,row_start,format_name = 'normal'):
        cell_start = 0
        for cell in cells:
            sheet.write(row_start,cell_start,cell,formats[format_name])
            cell_start += 1


        
    def generate_xlsx_report(self, workbook, data, recs):
        sheet_1 = workbook.add_worksheet("Report")
        formats = self.get_formats_dict(workbook)
        self.write_lines(sheet_1,formats,recs)