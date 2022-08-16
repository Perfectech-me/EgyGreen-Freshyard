from odoo import models, fields, api
class PortLoading(models.Model):
    _name = 'port.loading'
    _rec_name = 'name'
    _description = 'Port Of Loading'

    name = fields.Char(String="Name")
    port_sequence = fields.Char()
    street = fields.Char(string="Street")
    state_city_id = fields.Many2one(comodel_name="res.country.state")
    zip = fields.Char(string="zip")
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    shipping_type = fields.Selection(string="Shipping Type", selection=[('Air', 'Air'), ('Ocean', 'Ocean'),('Land', 'Land')],default='Air')


    @api.model
    def create(self, vals):
        """Add sequence."""
        vals.update({'port_sequence': self.env['ir.sequence'].next_by_code('port.loading.seq')})
        res = super(PortLoading, self).create(vals)

        return res




