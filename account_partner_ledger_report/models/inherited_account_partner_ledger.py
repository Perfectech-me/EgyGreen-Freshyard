# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import  timedelta
from odoo.tools import float_is_zero

class report_account_partner_ledger(models.AbstractModel):
    _inherit = "account.partner.ledger"

    filter_currency = True

    @api.model
    def _get_options_domain(self, options):
        domain = super(report_account_partner_ledger, self)._get_options_domain(options)

        if options.get('currency') and options.get('currency_ids'):
            domain += [
                ('currency_id','in',options.get('currency_ids') )
            ]

        return domain
