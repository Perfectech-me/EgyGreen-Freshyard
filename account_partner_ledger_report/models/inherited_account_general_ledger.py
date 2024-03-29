# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import  timedelta
from odoo.tools import float_is_zero
from odoo.exceptions import ValidationError
class report_account_partner_ledger(models.AbstractModel):
    _inherit = "account.general.ledger"

    filter_currency_2 = True
    filter_currency = [{'id':1, 'name': 'EUR', 'selected': False},{'id':2, 'name': 'USD', 'selected': False},{'id':74, 'name': 'EGP', 'selected': False},{'id':142, 'name': 'GBP', 'selected': False},]
    @api.model
    def _get_account_title_line(self, options, account, amount_currency, debit, credit, balance, has_lines):
        unfold_all = self._context.get('print_mode') and not options.get('unfolded_lines')

        name = '%s %s' % (account.code, account.name)
        rate = amount_currency / (debit - credit) if  (debit - credit)  else 1

        columns = [
            {'name': self.format_value(debit), 'class': 'number'},
            {'name': self.format_value(credit), 'class': 'number'},
            {'name': self.format_value(balance ), 'class': 'number'},
            {'name': self.format_value(balance * rate ,currency=account.currency_id), 'class': 'number'},
            
        ]
        if self.user_has_groups('base.group_multi_currency'):
            has_foreign_currency = account.currency_id and account.currency_id != account.company_id.currency_id or False
            columns.insert(0, {'name': has_foreign_currency and self.format_value(amount_currency, currency=account.currency_id, blank_if_zero=True) or '', 'class': 'number'})
        return {
            'id': 'account_%d' % account.id,
            'name': name,
            'code': account.code,
            'columns': columns,
            'level': 1,
            'unfoldable': has_lines,
            'unfolded': has_lines and 'account_%d' % account.id in options.get('unfolded_lines') or unfold_all,
            'colspan': 4,
            'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
        }

    @api.model
    def _get_columns_name(self, options):
        columns_names = [
            {'name': ''},
            {'name': _('Date'), 'class': 'date'},
            {'name': _('Communication')},
            {'name': _('Partner')},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'},
            {'name': _('Balance'), 'class': 'number'},
            {'name': _('Balance Currency'), 'class': 'number'},
            
        ]
        if self.user_has_groups('base.group_multi_currency'):
            columns_names.insert(4, {'name': _('Currency'), 'class': 'number'})
        return columns_names
    @api.model
    def _get_initial_balance_line(self, options, account, amount_currency, debit, credit, balance):
        rate = amount_currency / (debit - credit) if  (debit - credit)  else 1
        
        columns = [
            {'name': self.format_value(debit), 'class': 'number'},
            {'name': self.format_value(credit), 'class': 'number'},
            {'name': self.format_value(balance), 'class': 'number'},
            {'name': self.format_value(balance * rate,currency=account.currency_id), 'class': 'number'},
            
        ]

        if self.user_has_groups('base.group_multi_currency'):
            has_foreign_currency = account.currency_id and account.currency_id != account.company_id.currency_id or False
            columns.insert(0, {'name': has_foreign_currency and self.format_value(amount_currency, currency=account.currency_id, blank_if_zero=True) or '', 'class': 'number'})
        return {
            'id': 'initial_%d' % account.id,
            'class': 'o_account_reports_initial_balance',
            'name': _('Initial Balance'),
            'parent_id': 'account_%d' % account.id,
            'columns': columns,
            'colspan': 4,
        }
    @api.model
    def _get_aml_line(self, options, account, aml, cumulated_balance):
        if aml['payment_id']:
            caret_type = 'account.payment'
        else:
            caret_type = 'account.move'
        rate = aml['amount_currency'] / (aml['debit'] - aml['credit']) if  (aml['debit'] - aml['credit'])  else 1
        columns = [
            {'name': self.format_report_date(aml['date']), 'class': 'date'},
            {'name': self._format_aml_name(aml['name'], aml['ref']), 'class': 'o_account_report_line_ellipsis'},
            {'name': aml['partner_name'], 'class': 'o_account_report_line_ellipsis'},
            {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(cumulated_balance), 'class': 'number'},
            {'name': self.format_value(cumulated_balance * rate,currency=self.env['res.currency'].browse(aml['currency_id'])), 'class': 'number'},
            
        ]
        if self.user_has_groups('base.group_multi_currency'):
            if (aml['currency_id'] and aml['currency_id'] != account.company_id.currency_id.id) or account.currency_id:
                currency = self.env['res.currency'].browse(aml['currency_id'])
            else:
                currency = False
            columns.insert(3, {'name': currency and aml['amount_currency'] and self.format_value(aml['amount_currency'], currency=currency, blank_if_zero=True) or '', 'class': 'number'})
        return {
            'id': aml['id'],
            'caret_options': caret_type,
            'parent_id': 'account_%d' % aml['account_id'],
            'name': aml['move_name'],
            'columns': columns,
            'level': 2,
        }
    @api.model
    def _get_account_total_line(self, options, account, amount_currency, debit, credit, balance):

        columns = []
        if self.user_has_groups('base.group_multi_currency'):
            has_foreign_currency = account.currency_id and account.currency_id != account.company_id.currency_id or False
            columns.append({'name': has_foreign_currency and self.format_value(amount_currency, currency=account.currency_id, blank_if_zero=True) or '', 'class': 'number'})
        rate = amount_currency / (debit - credit) if  (debit - credit)  else 1
        columns += [
            {'name': self.format_value(debit), 'class': 'number'},
            {'name': self.format_value(credit), 'class': 'number'},
            {'name': self.format_value(balance), 'class': 'number'},
            {'name': self.format_value(balance * rate,currency=account.currency_id), 'class': 'number'},
            
        ]

        return {
            'id': 'total_%s' % account.id,
            'class': 'o_account_reports_domain_total',
            'parent_id': 'account_%s' % account.id,
            'name': _('Total %s', account["display_name"]),
            'columns': columns,
            'colspan': 4,
        }
    @api.model
    def _get_total_line(self, options, debit, credit, balance):
        currency = self.get_currency_id(options) or self.env.company.currency_id
        rate = 1 / currency._convert(
            1,
            self.env.company.currency_id,
            self.env.company,
            fields.Date.context_today(self),
        ) if self.get_currency_id(options) else 1
        return {
            'id': 'general_ledger_total_%s' % self.env.company.id,
            'name': _('Total'),
            'class': 'total',
            'level': 1,
            'columns': [
                {'name': self.format_value(debit), 'class': 'number'},
                {'name': self.format_value(credit), 'class': 'number'},
                {'name': self.format_value(balance), 'class': 'number'},
                {'name': self.format_value(balance * rate,currency = currency), 'class': 'number'},
                
            ],
            'colspan': self.user_has_groups('base.group_multi_currency') and 5 or 4,
        }
    def get_currency_id(self,options):
        currency_id = 0
        for c in options.get('currency',[]):
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
        for c in options.get('currency',[]):
            if c['selected']:
                currency_id = c['id']
        if currency_id:
            domain += [
                ('currency_id','=',currency_id )
            ]

        return domain
