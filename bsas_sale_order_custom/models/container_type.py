from odoo import models, fields, api

class ContainerType(models.Model):
    _name = 'container.type.config'
    _rec_name = 'name'
    _description = 'Container Type'

    # type = fields.Selection(string="Type", selection=[('Air', 'Air'), ('Ocean', 'Ocean'),('Land', 'Land')],default='Air')
    name = fields.Char(string="Name" )