from odoo import models, fields, api,_


class AccountMoveLine(models.Model):
    _inherit='account.move.line'
    currency_rate = fields.Float(string='Currency Rate', compute="_currency_rate" )

    def _currency_rate(self):
        if self.currency_id:
            print("self.currency_id",self.currency_id)
            for r in self:

                currency_id = self.env['res.currency'].search([('id', '=', r.currency_id.id)])
                for cur in currency_id:
                    if cur.rate_ids:

                     if cur.rate_ids[0].company_rate:

                      r.currency_rate =cur.rate_ids[0].inverse_company_rate
                    else:   r.currency_rate=1.0


        else:
            self.currency_rate = 1.0


