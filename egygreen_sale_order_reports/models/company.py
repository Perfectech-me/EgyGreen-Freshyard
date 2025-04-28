from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'res.company'
    company_qr = fields.Binary()
    stamp_image = fields.Binary(string="Stamp Image")
    signature_image = fields.Binary(string="Signature Image")
    report_logo = fields.Binary(string="Custom Report Logo")
