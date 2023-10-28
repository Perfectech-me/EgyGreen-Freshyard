from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'res.company'
    company_qr = fields.Binary()

