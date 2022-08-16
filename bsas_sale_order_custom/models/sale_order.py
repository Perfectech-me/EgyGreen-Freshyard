from odoo import models, fields, api
from datetime import datetime,date,timedelta

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def _default_validity_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
            days = self.env.company.quotation_validity_days
            if days > 0:
                return fields.Date.to_string(datetime.now() + timedelta(days))
        return False

    state = fields.Selection([

        ('pro_quotation', 'Proforma Quotation'),
        ('to_approve', 'TO Approve'),
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='pro_quotation')

    refuse_reason = fields.Text(string="Refuse Reason")


    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'pro_quotation': [('readonly', False)],'to_approve': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=True, readonly=True, states={'pro_quotation': [('readonly', False)],'to_approve': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=1,
        help="If you change the pricelist, only newly added lines will be affected.")

    validity_date = fields.Date(string='Expiration', readonly=True, copy=False,
                                states={'pro_quotation': [('readonly', False)],'to_approve': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                default=_default_validity_date)
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'pro_quotation': [('readonly', False)],'to_approve': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    order_category = fields.Selection(string="Order Catrgory", selection=[
                                                                            ('International', 'International'),
                                                                            ('Local', 'Local'),
                                                                            ('Export', 'Export'),
                                                                          ],default='International' )

    export_type = fields.Selection(string="Export Type", selection=[('fresh', 'Fresh'),('frozen','Frozen'), ('food_products', 'Food Products'),('other','Other') ],default='fresh')
    product_type = fields.Selection(string="Product Type", selection=[
        ('row_materials', 'Row Materials'),('sort','Sort'),('packing','Packing'), ('finish_products', 'Finish Products'),('other','Other') ],default='row_materials')

    shipping_type = fields.Selection(string="Shipping Type", selection=[('Air', 'Air'), ('Ocean', 'Ocean'),('Land', 'Land')],default='Air')
    deprture_date = fields.Date(string="departure date(ETD)")

    discharge_country_id = fields.Many2one(comodel_name="res.country", string="Place Of Discharge")
    discharge_city_id = fields.Many2one(comodel_name="res.country.state")

    final_destination_country_id = fields.Many2one(comodel_name="res.country", string="Final Destination")
    final_destination_city_id = fields.Many2one(comodel_name="res.country.state")

    port_loading_id = fields.Many2one(comodel_name="port.loading", string="Port Of Loading")

    origin_country_id = fields.Many2one(comodel_name="res.country", string="Country Of Origin")

    partner_notify_ids = fields.Many2many(comodel_name="res.partner", relation="notify_id", column1="notify_col1", column2="notify_col2", string="Notify")
    partner_notify_filters_ids = fields.Many2many(comodel_name="res.partner", relation="notify_filter_id", column1="notify_filter_col1", column2="notify_filter_col2",compute="_get_partner_notify_filters")

    partner_consignee_ids = fields.Many2many(comodel_name="res.partner", relation="consignee_id", column1="consignee_col1", column2="consignee_col2", string="consignee")
    partner_consignee_filters_ids = fields.Many2many(comodel_name="res.partner", relation="consignee_filters_id", column1="consignee_filters_col1", column2="consignee_filters_col2",compute="_get_partner_notify_filters")
    packing_place_id = fields.Many2one(comodel_name="res.partner", string="Packing Place")
    notify_partner_line = fields.One2many(comodel_name="res.partner.notify", inverse_name="sale_id",string="Notify Partner PO")
    consignee_partner_line = fields.One2many(comodel_name="res.partner.consignee", inverse_name="sale_id",string="Consignee Partner PO")
    loading_date = fields.Date(string="Loading Date")
    shipment_line_id = fields.Many2one(comodel_name="shipment.line", string="Shipment Line")
    sales_person_user_id = fields.Many2one(comodel_name="sales.person.users", string="Sales Person")
    bank_ids = fields.Many2many(comodel_name="res.partner.bank",string="Bank Accounts")


    @api.onchange('partner_id')
    def _get_partner_bank(self):
        for rec in self:
            bank=[]
            for line in rec.partner_id.bank_ids:
                bank.append(line.id)
            rec.bank_ids=bank

    @api.depends('partner_id')
    def _get_partner_notify_filters(self):
        for rec in self:
            partner_notify_filters=[]
            consignee_list=[]
            rec.partner_notify_filters_ids=False
            rec.partner_consignee_filters_ids=False
            if rec.partner_id.child_ids:
                for line in rec.partner_id.child_ids:
                    if line.type == 'invoice':
                        partner_notify_filters.append(line.id)
                    if line.type == 'delivery':
                        consignee_list.append(line.id)


                rec.partner_notify_filters_ids=partner_notify_filters
                rec.partner_consignee_filters_ids=consignee_list




    def button_quotation(self):
        for rec in self:
            rec.state = 'to_approve'


    def button_to_approve(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'approve.credit.limit',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
            }

    @api.onchange('port_loading_id')
    def _get_shipping_type(self):
        for rec in self:
            rec.shipping_type = rec.port_loading_id.shipping_type


    def button_set_to_proforma_quotation(self):
        for rec in self:
            rec.state='pro_quotation'



    @api.onchange('partner_notify_ids')
    def _get_notify_partner_line(self):
        lines = [(5, 0, 0)]
        if self.partner_notify_ids:
            for lin in self.partner_notify_ids:
                lines.append((0,0,{
                    'partner_id':lin._origin.id,
                }))
        self.update({'notify_partner_line':lines})

    @api.onchange('partner_consignee_ids')
    def _get_consignee_partner_line(self):
        lines = [(5, 0, 0)]
        if self.partner_consignee_ids:
            for lin in self.partner_consignee_ids:
                lines.append((0, 0, {
                    'partner_id': lin._origin.id,
                }))
        self.update({'consignee_partner_line': lines})


class ResPartnerNotify(models.Model):
    _name = 'res.partner.notify'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Name")
    notify_po = fields.Text(string="Notify Po")
    sale_id = fields.Many2one(comodel_name="sale.order" )

class ResPartnerConsignee(models.Model):
    _name = 'res.partner.consignee'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Name")
    consignee_po = fields.Text(string="Consignee Po")
    sale_id = fields.Many2one(comodel_name="sale.order" )




class SaleAdvancePaymentInvInherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    def create_invoices(self):
        res=super(SaleAdvancePaymentInvInherit, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if sale_orders:
            for sale in sale_orders:
                if sale.invoice_ids:
                    for inv in sale.invoice_ids:
                        if not inv.invoice_person_user_id:
                            inv.invoice_person_user_id=sale.sales_person_user_id.id
                        if not inv.bank_ids:
                            inv.bank_ids=sale.bank_ids.ids



        return res