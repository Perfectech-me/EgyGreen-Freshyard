from odoo import models, fields, api
class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    tax_commission_file_no = fields.Char(string="Tax Commission File No")

