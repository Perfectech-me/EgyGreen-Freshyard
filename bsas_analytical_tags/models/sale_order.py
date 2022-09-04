from odoo import models, fields, api,_
from datetime import datetime,date,timedelta
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def set_analytic_tag(self):
        if not self.analytic_account_id.id:
            raise ValidationError(
                _("Please Insert Analytic Account")
            )

        analytic_tag=self.env['account.analytic.tag'].sudo().create(
            {'name': self.name, 'active_analytic_distribution': True, 'company_id': self.company_id.id,
             'analytic_distribution_ids': [(0, 0, {'account_id': self.analytic_account_id.id, 'percentage': 1.0})]})
        for rec in self:
            print('rec.analytic_account_id.id',rec.analytic_account_id.name)
            for par in rec.order_line:
                if par.analytic_tag_ids:
                     analytic_tag=par.analytic_tag_ids



            for par in rec.order_line:
                if not par.analytic_tag_ids:
                   par.analytic_tag_ids=analytic_tag


