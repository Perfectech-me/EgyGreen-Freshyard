from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

from dateutil.relativedelta import relativedelta


class AccountPaymentTermLine(models.Model):
    _inherit = "account.payment.term.line"

    option = fields.Selection([
        ('day_after_invoice_date', "Days after the invoice date"),
        ('after_invoice_month', "Days after the end of the invoice month"),
        ('day_following_month', "Of the following month"),
        ('day_current_month', "Of the current month"),
        ('eta_delivery_date', "Delivery Date (ETA)"),
    ], default='day_after_invoice_date', required=True, string='Options')


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    def compute(self, value, date_ref=False, currency=None):
        self.ensure_one()
        date_ref = date_ref or fields.Date.context_today(self)
        amount = value
        sign = value < 0 and -1 or 1
        result = []
        if not currency and self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        elif not currency:
            currency = self.env.company.currency_id
        for line in self.line_ids:
            if line.value == 'fixed':
                amt = sign * currency.round(line.value_amount)
            elif line.value == 'percent':
                amt = currency.round(value * (line.value_amount / 100.0))
            elif line.value == 'balance':
                amt = currency.round(amount)
            next_date = fields.Date.from_string(date_ref)

            if line.option == 'eta_delivery_date':
                if self.env.context.get('commitment_date'):
                    commitment_date = fields.Date.from_string(self.env.context['commitment_date'])
                    next_date = commitment_date
                else:
                    # Fallback to the default behavior when no commitment_date is provided
                    next_date += relativedelta(days=line.days)
                    if line.day_of_the_month > 0:
                        months_delta = (line.day_of_the_month < next_date.day) and 1 or 0
                        next_date += relativedelta(day=line.day_of_the_month, months=months_delta)
            else:
                if line.option == 'day_after_invoice_date':
                    next_date += relativedelta(days=line.days)
                    if line.day_of_the_month > 0:
                        months_delta = (line.day_of_the_month < next_date.day) and 1 or 0
                        next_date += relativedelta(day=line.day_of_the_month, months=months_delta)
                elif line.option == 'after_invoice_month':
                    next_first_date = next_date + relativedelta(day=1, months=1)  # Getting 1st of next month
                    next_date = next_first_date + relativedelta(days=line.days - 1)
                elif line.option == 'day_following_month':
                    next_date += relativedelta(day=line.days, months=1)
                elif line.option == 'day_current_month':
                    next_date += relativedelta(day=line.days, months=0)

            result.append((fields.Date.to_string(next_date), amt))
            amount -= amt

        amount = sum(amt for _, amt in result)
        dist = currency.round(value - amount)
        if dist:
            last_date = result and result[-1][0] or fields.Date.context_today(self)
            result.append((last_date, dist))

        return sorted(result, key=lambda k: k[0])
