from odoo import models, fields, api
from odoo.tests import Form

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


    partner_shipping_ids = fields.Many2many(comodel_name="res.partner", relation="shipping_id", column1="part_shipping", column2="colum_shipping", string="Freight Forwarder", )
    partner_clearance_ids = fields.Many2many(comodel_name="res.partner", relation="clearance_id", column1="part_clearance", column2="colum_clearance", string="Clearance Company", )
    partner_insurance_ids = fields.Many2many(comodel_name="res.partner", relation="insurance_id", column1="part_insurance", column2="colum_insurance", string="Insurance Company", )

    container_number = fields.Float(string="Container/Equipment Quantity")
    free_duamrage = fields.Integer(string="Free Duamrage")
    cold_treatment = fields.Selection(string="Cold Treatment", selection=[('yes', 'Yes'), ('No', 'No'), ],default='yes')
    genest = fields.Selection(string="Genest", selection=[('yes', 'Yes'), ('No', 'No'), ],default='yes')

    def button_add_product_additional_cost(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'product.additional.cost',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
        }


    def action_confirm(self):
        res=super(SaleOrderInherit, self).action_confirm()
        for rec in self:

            partner_shipping=[]
            partner_clearance=[]
            partner_insurance=[]



            all_partners=[]
            for par in rec.order_line:
                if par.service_provider_partner_id.shipping_company:
                    partner_shipping.append(par.service_provider_partner_id.id)
                if par.service_provider_partner_id.clearance_company:
                    partner_clearance.append(par.service_provider_partner_id.id)
                if par.service_provider_partner_id.insurance_company:
                    partner_insurance.append(par.service_provider_partner_id.id)



                all_partners.append(par.service_provider_partner_id.id)


            rec.partner_shipping_ids=partner_shipping
            rec.partner_clearance_ids=partner_clearance
            rec.partner_insurance_ids=partner_insurance


            partners_records=self.env['res.partner'].search([('id','in',all_partners)])
            if partners_records:
                for partner in partners_records:
                    order_lines=[]
                    for line in rec.order_line:
                        if partner.id == line.service_provider_partner_id.id:
                            order_lines.append((0,0,{
                                'product_id':line.product_id.id,
                                'name':line.name,
                                'product_qty':line.product_uom_qty,
                                'price_unit':line.price_unit,
                                'taxes_id':line.tax_id.ids,
                            }))
                    self.env['purchase.order'].create({
                        'partner_id':partner.id,
                        'order_line':order_lines,

                    })

        return res


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    additional_service = fields.Boolean(string="Additional Service")
    shipping_product = fields.Boolean(string="Shipping Product")
    clearance_product = fields.Boolean(string="Clearance Product")
    insurance_product = fields.Boolean(string="Insurance Product")
    other_product = fields.Boolean(string="Other")
    partners_ids = fields.Many2many(comodel_name="res.partner",string="Partners",compute='compute_partners_ids')

    temperature = fields.Char(string="Temperature")
    humidity = fields.Char(string="Humidity")
    ventilation = fields.Char(string="Ventilation")



    @api.onchange('additional_service')
    def _check_product_services(self):
        self.shipping_product=False
        self.clearance_product=False
        self.insurance_product=False
        self.other_product=False

    @api.depends('shipping_product','clearance_product','insurance_product')
    def compute_partners_ids(self):
        for rec in self:
            rec.partners_ids=False
            domain = [('company_id', '=', rec.company_id.id)]
            if rec.shipping_product:
                domain.append(('shipping_company','=',True))
            if rec.clearance_product:
                domain.append(('clearance_company','=',True))
            if rec.insurance_product:
                domain.append(('insurance_company','=',True))
            rec.partners_ids=self.env['res.partner'].search(domain)


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    @api.onchange('additional_service')
    def _check_product_services(self):
        self.shipping_product = False
        self.clearance_product = False
        self.insurance_product = False
        self.other_product = False




class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    service_provider_partner_id = fields.Many2one(comodel_name="res.partner", string="Service Provider" )
    partners_ids = fields.Many2many(comodel_name="res.partner",string="Partners",related='product_id.partners_ids')


