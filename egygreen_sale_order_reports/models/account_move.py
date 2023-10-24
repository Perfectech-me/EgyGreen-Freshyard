from odoo import models, fields, api


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    no_of_pallets = fields.Char(string="No of Pallets")
    no_of_cartons = fields.Char(string="No of Cartons")
    hs_code = fields.Char(string="HS Code")
    ip_number = fields.Char(string="IP Number")
    irc_no = fields.Char(string="IRC No")
    partial_shipments = fields.Char(string="Partial Shipments")
    transshipment = fields.Char(string="Transshipment")
    lc_no = fields.Char(string="LC No")
    lc_date = fields.Char(string="LC Date")
    lcaf_no = fields.Char(string="LCAF No")
    data_loger = fields.Text(string="Data Loger")
    container_equipment_number = fields.Char(string="Container Equipment Number")
    final_destination_country_id = fields.Many2one('res.country')
    discharge_country_id = fields.Many2one('res.country')

class AccountMoveInherit(models.Model):
    _inherit = 'account.move.line'
    no_of_cartons = fields.Char(string="No of Cartons")
    