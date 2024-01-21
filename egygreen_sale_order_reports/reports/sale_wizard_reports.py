from odoo import models, fields, api
import xlsxwriter


class PartnerLedgerReportXlsx(models.AbstractModel):
    _name = 'report.egygreen_sale_order_reports.sale_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#237aab', 'color': 'white'})

        header_format_lines = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter'})

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

        domain = [('date_order', '>=', partners.date_from), ('date_order', '<=', partners.date_to)]
        sale_order = self.env['sale.order'].search(domain)

        row = 1
        col = 0

        cells = ['Sales Order', 'Customer Name', ]
        if partners.report_type == 'f':
            cells.extend(['Continent', 'Country', 'Order Category', 'Order Type', 'Product Type', 'Order Type'])
        cells.extend(['Analytical  Account', 'Final Destination'])
        if partners.report_type == 'f':
            cells.extend(['port of loading', 'place of discharge'])
        if partners.report_type in ['f', 's']:
            cells.extend(['incoterm'])
        cells.extend(['loading date'])
        if partners.report_type in ['f', 's']:
            cells.extend(['ETA'])
        cells.extend(['Container / Equipment Quantity', 'Container Equipment Number'])  # Adjusted columns
        container_quantity_position = cells.index('Container / Equipment Quantity')

        if partners.report_type in ['f']:
            cells.extend(['Container / Equipment Type', 'total net weight / KG', 'total gross weight / KG'])
        if partners.report_type in ['f', 's']:
            cells.extend(['Price list', 'Amount In Currency', 'Amount In EGP'])

        if partners.report_type in ['f', 's']:
            cells.extend(['Payment Terms'])
        cells.extend(['Freight Forwarder'])
        if partners.report_type in ['f', 's']:
            cells.extend(['Clearance Company', 'Insurance Company'])
        cells.extend(['shipping Line'])
        if partners.report_type in ['f', 's']:
            cells.extend(['Shipping Type'])
        if partners.report_type in ['f', ]:
            cells.extend(['sales person'])
        if partners.report_type in ['f', 't', 's']:
            cells.extend(['Departure Date(ETD)'])  # Adjusted column
        if partners.report_type in ['f']:
            cells.extend(['Invoice Status'])
        if partners.report_type in ['f', 's']:
            cells.extend(['B/L NUM', 'FORM 13'])
        if partners.report_type in ['f', 's', 't']:
            cells.extend(['Final Invoice No'])

        ic = 0
        for cell in cells:
            worksheet.write(row, col + ic, cell, header_format)
            ic += 1
        row += 1

        total_container_quantity = 0  # Initialize total container quantity
        for line in sale_order:
            cells = [line.name or "", line.partner_id.name or ""]
            if partners.report_type == 'f':
                cells.extend([line.partner_id.continent or "", line.partner_id.country_id.name or "",
                              line.order_category or "", line.export_type or "", line.product_type or "",
                              line.packing_place_id.name or ""])
            cells.extend([line.analytic_account_id.name or "", line.final_destination_country_id.name or ""])
            if partners.report_type == 'f':
                cells.extend([line.port_loading_id.name or "", line.discharge_country_id.name or ""])
            if partners.report_type in ['f', 's']:
                cells.extend([line.incoterm.name or ""])
            cells.extend([str(line.loading_date) or ""])
            if partners.report_type in ['f', 's']:
                cells.extend([str(line.commitment_date) or ""])
            cells.extend([str(line.container_number) or ""])
            cells.extend([line.container_equipment_number or ""])  # Fetching from SaleOrderInherit model
            total_container_quantity += float(line.container_number) if line.container_number else 0
            if partners.report_type in ['f']:
                cells.extend([str(line.container_type_id.name) or "",
                              sum(rec.net_weight_per_unit * rec.product_uom_qty for rec in line.order_line) or "",
                              sum(rec.gross_weight_per_unit * rec.product_uom_qty for rec in line.order_line) or ""])
            name_freight = ''
            for fright in line.partner_shipping_ids:
                name_freight += fright.name + ""
            name_clearance = ''
            for clearance in line.partner_clearance_ids:
                name_clearance += clearance.name + ""
            name_insurance = ''
            for insurance in line.partner_insurance_ids:
                name_insurance += insurance.name + ""
            if partners.report_type in ['f', 's']:
                cells.extend([line.pricelist_id.name + "(" + line.pricelist_id.currency_id.name + ")" or "",
                              line.amount_total or 0, line.total_amount_egp or 0])
            if partners.report_type in ['f', 's']:
                cells.extend([line.sudo().payment_term_id.name or ""])
            cells.extend([name_freight])
            if partners.report_type in ['f', 's']:
                cells.extend([name_clearance, name_insurance])
            status = ''
            if line.invoice_status == 'no':
                status = "Nothing to Invoice"
            elif line.invoice_status == 'to invoice':
                status = "To Invoice"
            elif line.invoice_status == 'invoiced':
                status = "Fully Invoiced"
            cells.extend([line.shipment_line_id.name or ""])
            if partners.report_type in ['f', 's']:
                cells.extend([line.shipping_line_type or ""])
            if partners.report_type in ['f', ]:
                cells.extend([line.sales_person_user_id.name or ""])
            if partners.report_type in ['f', 't', 's']:
                cells.extend([str(line.deprture_date) or "", ])
            invoice = self.env['account.move'].search([('id', 'in', line.invoice_ids.ids)], limit=1)
            if partners.report_type in ['f']:
                cells.extend([invoice.state or ""])
            if partners.report_type in ['f', 's']:
                cells.extend([invoice.bl_awb or '', invoice.form13number or ''])
            if partners.report_type in ['f', 's', 't']:
                cells.extend([invoice.name or ''])
            ic = 0
            for cell in cells:
                worksheet.write(row, col + ic, cell, header_format_lines)
                ic += 1

            row += 1

        worksheet.write(row, col + container_quantity_position, total_container_quantity, header_format_lines)


