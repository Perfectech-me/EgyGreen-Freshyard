from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    bl_awb = fields.Char(string="BL/AWB")
    inspection1_partner_id = fields.Many2one(comodel_name="res.partner", string="Inspection 1")
    inspection2_partner_id = fields.Many2one(comodel_name="res.partner", string="Inspection 2")
    insurance_customer_id = fields.Many2one(comodel_name="res.partner", string="Insurance Customer")

    other_cost = fields.Char(string="Other Cost")
    other_cost_partner_id = fields.Many2one(comodel_name="res.partner")

    form13number = fields.Char(string="From13 Number")
    form13date = fields.Date(string="From13 Date")
    form13amount = fields.Float(string="From13 Amount")

    @api.constrains('bl_awb','form13number')
    def _check_bl_awb_form13number(self):
        for rec in self.search([('id','!=',self.id),('move_type' ,'=', 'out_invoice')]):

            if self.move_type=='out_invoice':
                if rec.bl_awb==self.bl_awb:
                    raise ValidationError(("bl_awb Must Be Unique And Exist in Invoice "+str(rec.name)))

                if rec.form13number==self.form13number :
                    raise ValidationError(("From13 Number Must Be Unique And Exist in Invoice "+str(rec.name)))

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    container_equipment_number = fields.Char(string="Container/Equipment Number")
    is_storable = fields.Boolean(string="IS Storable",compute='compute_is_storable')
    @api.depends('product_id')
    def compute_is_storable(self):
        for rec in self:
            rec.is_storable=False
            if rec.product_id.detailed_type=='product':
                rec.is_storable=True

    @api.constrains('container_equipment_number')
    def _check_bl_awb(self):
        for rec in self:
            for line in rec.search([('id', '!=', rec.id)]):
                if line.container_equipment_number == rec.container_equipment_number and rec.is_storable==line.is_storable==True and rec.move_id.move_type == 'out_invoice':
                    raise ValidationError(("container/Equipment Number Must Be Unique And Exist in Invoice " + str(line.move_id.name)))
