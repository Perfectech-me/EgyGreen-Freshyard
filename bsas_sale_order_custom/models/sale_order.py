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
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='pro_quotation')




    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'pro_quotation': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=True, readonly=True, states={'pro_quotation': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=1,
        help="If you change the pricelist, only newly added lines will be affected.")

    validity_date = fields.Date(string='Expiration', readonly=True, copy=False,
                                states={'pro_quotation': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                default=_default_validity_date)
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'pro_quotation': [('readonly', False)],'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    order_category = fields.Selection(string="Order Catrgory", selection=[('Export', 'Export'), ('Local', 'Local'),
                                                                          ],default='Export' )

    export_type = fields.Selection(string="Export Type", selection=[('fresh', 'fresh'),('frozen','frozen'), ('food_products', 'Food Products'), ],default='fresh')

    shipping_type = fields.Selection(string="Shipping Type", selection=[('Air', 'Air'), ('Ocean', 'Ocean'),('Land', 'Land')],default='Air')
    deprture_date = fields.Date(string="Departure Date (ADT)")

    discharge_country_id = fields.Many2one(comodel_name="res.country", string="Place Of Discharge")
    discharge_city_id = fields.Many2one(comodel_name="res.country.state")

    final_destination_country_id = fields.Many2one(comodel_name="res.country", string="Final Destination")
    final_destination_city_id = fields.Many2one(comodel_name="res.country.state")

    port_loading_id = fields.Many2one(comodel_name="port.loading", string="Port Of Loading")

    origin_country_id = fields.Many2one(comodel_name="res.country", string="Country Of Origin")

    @api.onchange('order_category')
    def _set_order_category_fields(self):
        for rec in self:
            rec.deprture_date=False
            rec.discharge_country_id=False
            rec.discharge_city_id=False
            rec.final_destination_country_id=False
            rec.final_destination_city_id=False
            rec.port_loading_id=False
            rec.origin_country_id=False
            rec.export_type=False


    def button_quotation(self):
        for rec in self:
            rec.state = 'draft'

    @api.onchange('port_loading_id')
    def _get_shipping_type(self):
        for rec in self:
            rec.shipping_type = rec.port_loading_id.shipping_type


    def button_set_to_proforma_quotation(self):
        for rec in self:
            rec.state='pro_quotation'