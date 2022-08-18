from odoo import models, fields, api

class RefuseCreditLimit(models.TransientModel):
    _name = 'refuse.credit.limit'

    refuse_reason = fields.Text(string="Refuse Reason")
    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale")

    def button_approve(self):
        print("GGGGGGGGGGGGGGGGGGGGGGGG",self.sale_id)
        self.sale_id.state='cancel'
        self.sale_id.refuse_reason=self.refuse_reason
