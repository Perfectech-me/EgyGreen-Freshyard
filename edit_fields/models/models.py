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


