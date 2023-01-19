from odoo import models, fields, api,_


class AccountMoveLine(models.Model):
    _inherit='account.move.line'
    currency_rate = fields.Float(string='Currency Rate', compute="_currency_rate" )

    @api.depends('currency_id','date')
    def _currency_rate(self):
        for rec in self:
            rec.currency_rate = 0.0
            rates_current = []
            rate = 0
            if rec.currency_id:
                rates = rec.currency_id.rate_ids.mapped('name')
                for line in rates:
                    if line <= rec.date:
                        rates_current.append(line)
                for line in rec.currency_id.rate_ids:
                    if rates_current and max(set(rates_current)) == line.name:
                        rec.currency_rate = line.inverse_company_rate





