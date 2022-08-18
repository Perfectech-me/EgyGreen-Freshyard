from odoo import models, fields, api
class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    shipping_company = fields.Boolean(string="Shipping Product")
    clearance_company = fields.Boolean(string="Clearance Product")
    insurance_company = fields.Boolean(string="Insurance Product")

