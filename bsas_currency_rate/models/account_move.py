from odoo import models, fields, api,_


class AccountMoveLine(models.Model):
    _inherit='account.move.line'
    currency_rate = fields.Float(string='Currency Rate', compute="_currency_rate" )

    def _currency_rate(self):
        print("curren1",self.currency_id.id)

        currency_id = self.env['res.currency'].search([('id', '=', self.currency_id.id)])
        for cur in currency_id:
            if cur.rate_ids:

             if cur.rate_ids[0].company_rate:
              self.currency_rate =cur.rate_ids[0].company_rate
            else:   self.currency_rate=0.0




