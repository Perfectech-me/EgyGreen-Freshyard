# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import  timedelta
from odoo.tools import float_is_zero
from odoo.exceptions import ValidationError
class report_account_partner_ledger(models.AbstractModel):
    _inherit = "account.partner.ledger"

    filter_currency_2 = True
    filter_currency = [{'id':1, 'name': 'EUR', 'selected': False},{'id':2, 'name': 'USD', 'selected': False},{'id':74, 'name': 'EGP', 'selected': False},{'id':142, 'name': 'GBP', 'selected': False},]
    @api.model
    def _get_report_line_total(self, options, initial_balance, debit, credit, balance,total_currency):
        vals = super()._get_report_line_total(options, initial_balance, debit, credit, balance)
        vals['columns'][-2] = {'name': self.format_value(total_currency,currency = self.get_currency_id(options)), 'class': 'number'}

        return vals

    @api.model
    def _get_report_line_partner(self, options, partner, initial_balance, debit, credit, balance,amount_currency):
        vals = super()._get_report_line_partner( options, partner, initial_balance, debit, credit, balance)
        vals['columns'][-2] = {'name': self.format_value(amount_currency,currency = self.get_currency_id(options)), 'class': 'number'}

        return vals

    @api.model
    def _get_partner_ledger_lines(self, options, line_id=None):
        ''' Get lines for the whole report or for a specific line.
        :param options: The report options.
        :return:        A list of lines, each one represented by a dictionary.
        '''
        lines = []
        unfold_all = options.get('unfold_all') or (self._context.get('print_mode') and not options['unfolded_lines'])

        expanded_partner = line_id and self.env['res.partner'].browse(int(line_id[8:]))
        partners_results = self._do_query(options, expanded_partner=expanded_partner)

        total_initial_balance = total_debit = total_credit = total_balance  = total_currency = 0.0
        for partner, results in partners_results:
            partner_total_currency = 0
            is_unfolded = 'partner_%s' % (partner.id if partner else 0) in options['unfolded_lines']
            cur_lines = results.get('lines',[])
            if not cur_lines:
                query, params = self._get_query_amls(options, expanded_partner=partner)
                self._cr.execute(query, params)
                for res in self._cr.dictfetchall():
                    cur_lines.append(res)
            for cur_line in cur_lines:
                total_currency += cur_line['amount_currency']
                partner_total_currency += cur_line['amount_currency']
            # res.partner record line.
            partner_sum = results.get('sum', {})
            partner_init_bal = results.get('initial_balance', {})

            initial_balance = partner_init_bal.get('balance', 0.0)
            debit = partner_sum.get('debit', 0.0)
            credit = partner_sum.get('credit', 0.0)
            balance = initial_balance + partner_sum.get('balance', 0.0)

            lines.append(self._get_report_line_partner(options, partner, initial_balance, debit, credit, balance,partner_total_currency))

            total_initial_balance += initial_balance
            total_debit += debit
            total_credit += credit
            total_balance += balance

            if unfold_all or is_unfolded:
                cumulated_balance = initial_balance

                # account.move.line record lines.
                amls = results.get('lines', [])

                load_more_remaining = len(amls)
                load_more_counter = self._context.get('print_mode') and load_more_remaining or self.MAX_LINES

                for aml in amls:
                    # Don't show more line than load_more_counter.
                    if load_more_counter == 0:
                        break

                    cumulated_init_balance = cumulated_balance
                    cumulated_balance += aml['balance']
                    lines.append(self._get_report_line_move_line(options, partner, aml, cumulated_init_balance, cumulated_balance))

                    load_more_remaining -= 1
                    load_more_counter -= 1

                if load_more_remaining > 0:
                    # Load more line.
                    lines.append(self._get_report_line_load_more(
                        options,
                        partner,
                        self.MAX_LINES,
                        load_more_remaining,
                        cumulated_balance,
                    ))

        if not line_id:
            # Report total line.
            lines.append(self._get_report_line_total(
                options,
                total_initial_balance,
                total_debit,
                total_credit,
                total_balance,
                total_currency
            ))
        return lines
    def get_currency_id(self,options):
        currency_id = 0
        for c in options['currency']:
            if c['selected']:
                currency_id = c['id']
        currency = self.env.company.currency_id
        if currency_id:
            currency = self.env['res.currency'].browse(currency_id)
        return currency
    @api.model
    def _get_options_domain(self, options):
        domain = super(report_account_partner_ledger, self)._get_options_domain(options)
        currency_id = 0
        for c in options['currency']:
            if c['selected']:
                currency_id = c['id']
        if currency_id:
            domain += [
                ('currency_id','=',currency_id )
            ]

        return domain
