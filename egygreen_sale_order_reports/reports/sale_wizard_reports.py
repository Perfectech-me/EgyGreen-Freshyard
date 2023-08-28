from odoo import models, fields, api
from odoo import models
import datetime
from datetime import date, datetime, time, timedelta
from pytz import timezone
import xlsxwriter


class PartnerLedgerReportXlsx(models.AbstractModel):
    _name = 'report.egygreen_sale_order_reports.sale_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#237aab', 'color': 'white'})

        header_format_lines = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter'})



        format_total_lines = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter','bg_color': '#b3b3b3','color': 'white'})

        worksheet = workbook.add_worksheet('Sale Order')

        worksheet.set_column('A:A', 22)
        worksheet.set_column('B:B', 22)
        worksheet.set_column('C:C', 22)
        worksheet.set_column('D:D', 22)
        worksheet.set_column('E:E', 22)
        worksheet.set_column('G:G', 22)
        worksheet.set_column('F:F', 22)
        worksheet.set_column('H:H', 22)
        worksheet.set_column('I:I', 22)
        worksheet.set_column('J:J', 22)
        worksheet.set_column('K:K', 22)
        worksheet.set_column('L:L', 22)
        worksheet.set_column('M:M', 22)
        worksheet.set_column('N:N', 22)
        worksheet.set_column('O:O', 22)
        worksheet.set_column('P:P', 22)
        worksheet.set_column('Q:Q', 22)
        worksheet.set_column('R:R', 22)
        worksheet.set_column('S:S', 22)
        worksheet.set_column('T:T', 22)
        worksheet.set_column('U:U', 22)
        worksheet.set_column('V:V', 22)
        worksheet.set_column('W:W', 22)
        worksheet.set_column('X:X', 22)
        worksheet.set_column('Y:Y', 22)
        worksheet.set_column('Z:Z', 22)
        worksheet.set_column('AA:AA', 22)
        worksheet.set_column('AB:AB', 22)
        worksheet.set_column('AC:AC', 22)
        worksheet.set_column('AD:AD', 22)
        worksheet.set_column('AE:AE', 22)


        domain=[('date_order','>=',partners.date_from),('date_order','<=',partners.date_to)]

        if partners.company_id:
            domain.append(('company_id', '=', partners.company_id.id))

        if partners.invoice_status:
            domain.append(('invoice_status', '=', partners.invoice_status))


        if partners.partner_ids:
            domain.append(('partner_id','in',partners.partner_ids.ids))
        #
        if partners.continent:
            domain.append(('partner_id.continent','=',partners.continent))
        #
        if partners.country_ids:
            domain.append(('partner_id.country_id','=',partners.country_ids.ids))

        if partners.order_category:
            domain.append(('order_category','=',partners.order_category))
        #
        if partners.export_type:
            domain.append(('export_type', '=', partners.export_type))
        #
        if partners.packing_place_id:
            domain.append(('packing_place_id', '=', partners.packing_place_id.id))
        #
        if partners.analytic_account_id:
            domain.append(('analytic_account_id', '=', partners.analytic_account_id.id))

        if partners.discharge_country_id:
            domain.append(('discharge_city_id', '=', partners.discharge_country_id.id))

        if partners.incoterm_id:
            domain.append(('incoterm_id', '=', partners.incoterm_id.id))
        #
        if partners.pricelist_id:
            domain.append(('pricelist_id', '=', partners.pricelist_id.id))

        if partners.partner_shipping_ids:
            domain.append(('partner_shipping_ids', 'in', partners.partner_shipping_ids.ids))
        #
        if partners.partner_clearance_ids:
            domain.append(('partner_clearance_ids', 'in', partners.partner_clearance_ids.ids))

        if partners.partner_insurance_ids:
            domain.append(('partner_insurance_ids', 'in', partners.partner_insurance_ids.ids))
        #
        if partners.shipping_type:
            domain.append(('shipping_type', '=', partners.shipping_type))

        if partners.sales_person_user_ids:
            domain.append(('sales_person_user_id', 'in', partners.sales_person_user_ids.ids))
        #
        if partners.product_type:
            domain.append(('product_type', '=', partners.product_type))


        row = 1
        col = 0



        sale_order=self.env['sale.order'].search(domain)
        cells = ['Sales Order','Customer Name',]
        if partners.report_type == 'f':
            cells.extend(['Continent','Country','Order Category','Order Type','Product Type','Order Type'])
        cells.extend(['Analytical  Account','Final Destination'])
        if partners.report_type == 'f':
            cells.extend(['port of loading','place of discharge'])
        if partners.report_type in ['f','s']:
            cells.extend(['incoterm'])
        cells.extend(['loading date'])
        if partners.report_type in ['f','s']:
            cells.extend(['ETA'])
        cells.extend(['Container / Equipment Quantity'])
        if partners.report_type in ['f']:
            cells.extend(['Container / Equipment Type','total net weight / KG','total gross weight / KG'])
        if partners.report_type in ['f','s']:
            cells.extend(['Price list','Amount In Currency','Amount In EGP'])
            
        if partners.report_type in ['f','s']:
            cells.extend(['Payment Terms'])
        cells.extend(['Freight Forwarder'])
        if partners.report_type in ['f','s']:
            cells.extend(['Clearance Company','Insurance Company'])
        cells.extend(['shipping Line'])
        if partners.report_type in ['f','s']:
            cells.extend(['Shipping Type'])
        if partners.report_type in ['f',]:
            cells.extend(['sales person'])
        if partners.report_type in ['f','t','s']:
            cells.extend(['Container Equipment Number'])
        if partners.report_type in ['f','t','n']:
            cells.extend(['Departure Date(ETD)'])
        if partners.report_type in ['f']:
            cells.extend(['Invoice Status'])
        if partners.report_type in ['f','s']:
            cells.extend(['B/L NUM','FORM 13'])
        if partners.report_type in ['f','s','t']:
            cells.extend(['Final Invoice No'])
        ic = 0
        for cell in cells:
            worksheet.write(row, col + ic, cell, header_format)
            ic += 1
        row += 1
        for line in sale_order:
            cells = [line.name or "",line.partner_id.name or ""]
            if partners.report_type == 'f':
                cells.extend([line.partner_id.continent or "",line.partner_id.country_id.name or "",line.order_category or "",line.export_type or "",line.product_type or "",line.packing_place_id.name or ""])
            cells.extend([line.analytic_account_id.name or "",line.final_destination_country_id.name or ""])
            if partners.report_type == 'f':
                cells.extend([line.port_loading_id.name or "",line.discharge_country_id.name or ""])
            if partners.report_type in ['f','s']:
                cells.extend([line.incoterm.name or ""])
            cells.extend([str(line.loading_date) or ""])
            if partners.report_type in ['f','s']:
                cells.extend([str(line.commitment_date) or ""])
            cells.extend([str(line.container_number) or ""])
            if partners.report_type in ['f']:
                cells.extend([str(line.container_type_id.name) or "",sum(rec.net_weight_per_unit for rec in line.order_line)  or "",sum(rec.gross_weight_per_unit for rec in line.order_line)  or ""])
            name_freight=''
            for fright in line.partner_shipping_ids:
                name_freight+=fright.name+""
            name_clearance = ''
            for clearance in line.partner_clearance_ids:
                name_clearance += clearance.name + ""
            name_insurance = ''
            for insurance in line.partner_insurance_ids:
                name_insurance += insurance.name + ""
            if partners.report_type in ['f','s']:
                cells.extend([line.pricelist_id.name+"("+line.pricelist_id.currency_id.name+")"  or "", line.amount_total,line.total_amount_egp])
            if partners.report_type in ['f','s']:
                cells.extend([line.sudo().payment_term_id.name  or ""])
            cells.extend([name_freight])
            if partners.report_type in ['f','s']:
                cells.extend([name_clearance,name_insurance])
            status = ''
            if line.invoice_status=='no':
                status = "Nothing to Invoice"
            elif line.invoice_status=='to invoice':
                status = "To Invoice"
            elif line.invoice_status=='invoiced':
                status = "Fully Invoiced"
            cells.extend([line.shipment_line_id.name or ""])
            if partners.report_type in ['f','s']:
                cells.extend([line.shipping_line_type or ""])
            if partners.report_type in ['f',]:
                cells.extend([line.sales_person_user_id.name or ""])
            if partners.report_type in ['f','t','s']:
                cells.extend([line.order_line[0]['container_equipment_number']])
            if partners.report_type in ['f','t','n']:
                cells.extend([str(line.deprture_date) or "",])
            if partners.report_type in ['f']:
                cells.extend([])
            invoice = self.env['account.move'].search([('id','in',line.invoice_ids.ids)],limit = 1)
            if partners.report_type in ['f','s']:
                cells.extend([invoice.bl_awb or  '',invoice.form13number or ''])
            if partners.report_type in ['f','s','t']:
                cells.extend([invoice.name or ''])
            ic = 0
            for cell in cells:
                worksheet.write(row, col + ic, cell, header_format_lines)
                ic += 1

            row += 1
            # worksheet.write(row, col, 'Product Name', header_format)
            # worksheet.write(row, col + 1, 'Quantity', header_format)
            # worksheet.write(row, col + 2, 'Container Equipment Number', header_format)
            # worksheet.write(row, col + 3, 'Net Weight Per Unit', header_format)
            # worksheet.write(row, col + 4, 'Gross Weight Per Unit', header_format)
            # worksheet.write(row, col + 5, 'Price Unit', header_format)
            # worksheet.write(row, col + 6, 'Subtotal', header_format)
            # row += 1

            # for order_line in line.order_line:
            #
            #     worksheet.write(row, col, order_line.name, header_format_lines)
            #     worksheet.write(row, col+1, order_line.product_uom_qty, header_format_lines)
            #     worksheet.write(row, col+2, order_line.container_equipment_number, header_format_lines)
            #     worksheet.write(row, col+3, order_line.net_weight_per_unit, header_format_lines)
            #     worksheet.write(row, col+4, order_line.gross_weight_per_unit, header_format_lines)
            #     worksheet.write(row, col+5, order_line.price_unit, header_format_lines)
            #     worksheet.write(row, col+6, order_line.price_subtotal, header_format_lines)
            #
            #     row += 1
            # row += 1
            # string_a = 'A' + str(row + 1) + ':Y' + str(row + 1)
            # worksheet.merge_range(string_a, "", format_total_lines)
            # row += 2