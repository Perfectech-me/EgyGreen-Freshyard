from odoo import models, fields, api
class ResPArtnerType(models.Model):
    _name = 'res.partner.type'
    _rec_name = 'name'
    _description = 'customer Type'

    name = fields.Char()

