# -*- coding: utf-8 -*-
import base64

from num2words import num2words

from odoo import models, fields, api, _,tools
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'
    company_id = fields.Many2one('res.company', 'Company', index=True,required=True)



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _create_exchange_difference_move(self):
        res = super()._create_exchange_difference_move()
        if res:
            for move in res:
                for line in move.line_ids:
                    line.analytic_tag_ids = self.analytic_tag_ids
                    print('AAASSDD ',line)

        return res