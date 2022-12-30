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

        worksheet = workbook.add_worksheet('Journal Entries')

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


        domain=[('date_order','>=',partners.date_from),('date_order','<=',partners.date_to)]

        if partners.partner_ids:
            domain.append(('partner_id','in',partners.partner_ids.ids))

        if partners.continent:
            domain.append(('partner_id.continent','=',partners.continent))

        if partners.country_ids:
            domain.append(('partner_id.country_id','=',partners.country_ids.ids))
        if partners.order_category:
            domain.append(('order_category','=',partners.order_category))

        if partners.export_type:
            domain.append(('export_type', '=', partners.export_type))

        if partners.packing_place_id:
            domain.append(('packing_place_id', '=', partners.packing_place_id.id))

        if partners.analytic_account_id:
            domain.append(('analytic_account_id', '=', partners.analytic_account_id.id))
        if partners.discharge_country_id:
            domain.append(('discharge_country_id', '=', partners.discharge_country_id.id))

        if partners.incoterm_id:
            domain.append(('incoterm_id', '=', partners.incoterm_id.id))

        if partners.pricelist_id:
            domain.append(('pricelist_id', '=', partners.pricelist_id.id))

        if partners.partner_shipping_ids:
            domain.append(('partner_shipping_ids', 'in', partners.partner_shipping_ids.ids))

        if partners.partner_clearance_ids:
            domain.append(('partner_clearance_ids', 'in', partners.partner_clearance_ids.ids))

        if partners.partner_insurance_ids:
            domain.append(('partner_insurance_ids', 'in', partners.partner_insurance_ids.ids))

        if partners.shipping_type:
            domain.append(('shipping_type', '=', partners.shipping_type))

        if partners.sales_person_user_ids:
            domain.append(('sales_person_user_id', 'in', partners.sales_person_user_ids.ids))


        row = 1
        col = 0



        sale_order=self.env['sale.order'].search(domain)

        for line in sale_order:

            worksheet.write(row, col, 'Sales Order', header_format)
            worksheet.write(row, col + 1, 'Customer Name', header_format)
            worksheet.write(row, col + 2, 'Continent', header_format)
            worksheet.write(row, col + 3, 'Country', header_format)
            worksheet.write(row, col + 3, 'Order Category', header_format)
            worksheet.write(row, col + 4, 'Order Type', header_format)
            worksheet.write(row, col + 5, 'Product Type', header_format)
            worksheet.write(row, col + 6, 'Packing place', header_format)
            worksheet.write(row, col + 7, 'Analytical  Account', header_format)
            worksheet.write(row, col + 8, 'Final Destination', header_format)
            worksheet.write(row, col + 9, 'port of loading', header_format)
            worksheet.write(row, col + 10, 'place of discharge', header_format)
            worksheet.write(row, col + 11, 'incoterm', header_format)
            worksheet.write(row, col + 12, 'loading date', header_format)
            worksheet.write(row, col + 13, 'ETA', header_format)
            worksheet.write(row, col + 14, 'total net weight / KG', header_format)
            worksheet.write(row, col + 15, 'total gross weight / KG', header_format)
            worksheet.write(row, col + 16, 'Price list', header_format)
            worksheet.write(row, col + 17, 'Amount In Currency', header_format)
            worksheet.write(row, col + 22, 'amount in Egp', header_format)
            worksheet.write(row, col + 19, 'payment Terms', header_format)
            worksheet.write(row, col + 20, 'shipping Line', header_format)
            worksheet.write(row, col + 21, 'shipping Type', header_format)
            worksheet.write(row, col + 22, 'sales person', header_format)

            row += 1
            worksheet.write(row, col, line.name, header_format_lines)
            worksheet.write(row, col + 1, line.partner_id.name, header_format_lines)
            worksheet.write(row, col + 2, line.partner_id.continent, header_format_lines)
            worksheet.write(row, col + 3, line.partner_id.country_id.name, header_format_lines)
            worksheet.write(row, col + 3, line.order_category, header_format_lines)
            worksheet.write(row, col + 4, line.export_type, header_format_lines)
            worksheet.write(row, col + 5, line.product_type, header_format_lines)
            worksheet.write(row, col + 6, line.packing_place_id.name, header_format_lines)
            worksheet.write(row, col + 7, line.analytic_account_id.name, header_format_lines)
            worksheet.write(row, col + 8, line.final_destination_country_id.name, header_format_lines)
            worksheet.write(row, col + 9, line.port_loading_id.name, header_format_lines)
            worksheet.write(row, col + 10, line.discharge_country_id.name, header_format_lines)
            worksheet.write(row, col + 11, line.incoterm.name, header_format_lines)
            worksheet.write(row, col + 12, str(line.loading_date), header_format_lines)
            worksheet.write(row, col + 13, str(line.commitment_date), header_format_lines)
            worksheet.write(row, col + 14, sum(rec.net_weight_per_unit for rec in line.order_line), header_format_lines)
            worksheet.write(row, col + 15, sum(rec.gross_weight_per_unit for rec in line.order_line), header_format_lines)
            worksheet.write(row, col + 16, line.pricelist_id.name, header_format_lines)
            worksheet.write(row, col + 17, line.amount_total, header_format_lines)
            worksheet.write(row, col + 22, line.amount_total/line.currency_id.rate if line.currency_id.rate>0 else 0,header_format_lines)
            worksheet.write(row, col + 19, line.payment_term_id.name, header_format_lines)
            worksheet.write(row, col + 20, line.shipment_line_id.name, header_format_lines)
            worksheet.write(row, col + 21, line.shipping_line_type, header_format_lines)
            worksheet.write(row, col + 22, line.sales_person_user_id.name, header_format_lines)

            row += 1
            worksheet.write(row, col, 'Product Name', header_format)
            worksheet.write(row, col + 1, 'Quantity', header_format)
            worksheet.write(row, col + 2, 'Container Equipment Number', header_format)
            worksheet.write(row, col + 3, 'Net Weight Per Unit', header_format)
            worksheet.write(row, col + 4, 'Gross Weight Per Unit', header_format)
            worksheet.write(row, col + 5, 'Price Unit', header_format)
            worksheet.write(row, col + 6, 'Subtotal', header_format)
            row += 1

            for order_line in line.order_line:

                worksheet.write(row, col, order_line.name, header_format_lines)
                worksheet.write(row, col+1, order_line.product_uom_qty, header_format_lines)
                worksheet.write(row, col+2, order_line.container_equipment_number, header_format_lines)
                worksheet.write(row, col+3, order_line.net_weight_per_unit, header_format_lines)
                worksheet.write(row, col+4, order_line.gross_weight_per_unit, header_format_lines)
                worksheet.write(row, col+5, order_line.price_unit, header_format_lines)
                worksheet.write(row, col+6, order_line.price_subtotal, header_format_lines)

                row += 1
            row += 1
            string_a = 'A' + str(row + 1) + ':Y' + str(row + 1)
            worksheet.merge_range(string_a, "", format_total_lines)
            row += 2