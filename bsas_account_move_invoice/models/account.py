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
    without_holding_amount=fields.Float(compute='compute_without_holding_amount')
    rate_without_holding = fields.Float(compute='compute_without_holding_amount')

    @api.depends('invoice_line_ids')
    def compute_without_holding_amount(self):
        for rec in self:
            rec.without_holding_amount=0.0
            rec.rate_without_holding =0.0
            total_tax = 0.0
            for line in rec.invoice_line_ids:
                for tax in line.tax_ids:
                    if tax.without_holding:
                        if tax.amount<0:
                            total_tax+=((tax.amount*line.price_subtotal*-1)/100)
                        else:
                            total_tax+=((tax.amount*line.price_subtotal)/100)
                        rec.rate_without_holding=tax.amount

            rec.without_holding_amount = total_tax

    @api.constrains('bl_awb','form13number')
    def _check_bl_awb_form13number(self):
        for rec in self.search([('id','!=',self.id),('move_type' ,'=', 'out_invoice')]):

            if self.move_type=='out_invoice':
                if rec.bl_awb==self.bl_awb:
                    raise ValidationError(("bl_awb Must Be Unique And Exist in Invoice "+str(rec.name)))

                if rec.form13number==self.form13number :
                    raise ValidationError(("From13 Number Must Be Unique And Exist in Invoice "+str(rec.name)))



    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMoveInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                                  submenu=submenu)
        remove_report_id = self.env.ref('bsas_account_move_invoice.action_report_account_move_bill_discount').id
        if view_type == 'form' and self.env.context.get('default_move_type') !='in_invoice':
            if remove_report_id and toolbar and res['toolbar'] and res['toolbar'].get('print'):
                remove_report_record = [rec for rec in res['toolbar'].get('print') if rec.get('id') == remove_report_id]
                if remove_report_record and remove_report_record[0]:
                    res['toolbar'].get('print').remove(remove_report_record[0])
        return res




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
