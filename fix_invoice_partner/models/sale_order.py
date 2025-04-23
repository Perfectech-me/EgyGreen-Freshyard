# -*- coding: utf-8 -*-
import base64

from num2words import num2words

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def fix_invoice_partner_company(self):
        orders = self.search(
            [('partner_invoice_id.company_id', '!=', False)])
        for order in orders:
            partner = order.partner_id
            invoice_partner = order.partner_invoice_id
            shipping_partner = order.partner_shipping_id

            if not partner or not invoice_partner or not shipping_partner:
                print("not exits")
                continue
            if invoice_partner.company_id != partner.company_id:
                try:
                    invoice_partner.sudo().write({'company_id': partner.company_id.id})
                    print("updated")
                except Exception as e:
                    print("not updated")

            if shipping_partner.company_id != partner.company_id:
                try:
                    shipping_partner.sudo().write({'company_id': partner.company_id.id})
                    print("updated")
                except Exception as e:
                    print("not updated")

            if invoice_partner.company_id == partner.company_id and shipping_partner.company_id == partner.company_id:
                print("ok")
