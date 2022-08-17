from odoo import models, fields, api
class ResPArtnerTypes(models.Model):
    _name = 'res.partner.types'
    _rec_name = 'name'
    _description = 'customer Type'

    name = fields.Char()

