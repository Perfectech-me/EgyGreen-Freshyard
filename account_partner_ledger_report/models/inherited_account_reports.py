# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    filter_currency = None

    @api.model
    def _init_filter_currency(self, options, previous_options=None):
        if not self.filter_currency:
            return

        options['currency'] = True
        options['currency_ids'] = previous_options and previous_options.get('currency_ids') or []
        selected_currency_ids = [int(currency) for currency in options['currency_ids']]
        selected_currencys = selected_currency_ids and self.env['res.currency'].browse(selected_currency_ids) or self.env['res.currency']
        options['selected_currency_ids'] = selected_currencys.mapped('name')

    # def _set_context(self, options):
    #     ctx = super(AccountReport, self)._set_context(options)
    #     if options.get('account_ids'):
    #         ctx['account_ids'] = self.env['account.account'].browse(
    #             [int(account) for account in options['account_ids']])
    #     return ctx
    #
    #
    # def get_report_informations(self, options):
    #     if self._name != 'account.general.ledger':
    #         return super(AccountReport, self).get_report_informations(options)
    #     options = self._get_options(options)
    #
    #     searchview_dict = {'options': options, 'context': self.env.context}
    #     # Check if report needs analytic
    #     if options.get('analytic_accounts') is not None:
    #         options['selected_analytic_account_names'] = [self.env['account.analytic.account'].browse(int(account)).name for account in options['analytic_accounts']]
    #     if options.get('analytic_tags') is not None:
    #         options['selected_analytic_tag_names'] = [self.env['account.analytic.tag'].browse(int(tag)).name for tag in options['analytic_tags']]
    #     if options.get('partner'):
    #         options['selected_partner_ids'] = [self.env['res.partner'].browse(int(partner)).name for partner in options['partner_ids']]
    #         options['selected_partner_categories'] = [self.env['res.partner.category'].browse(int(category)).name for category in (options.get('partner_categories') or [])]
    #     if options.get('account'):
    #         options['selected_account_ids'] = [self.env['account.account'].browse(int(account)).name for account in
    #                                           options['account_ids']]
    #
    #     # Check whether there are unposted entries for the selected period or not (if the report allows it)
    #     if options.get('date') and options.get('all_entries') is not None:
    #         date_to = options['date'].get('date_to') or options['date'].get('date') or fields.Date.today()
    #         period_domain = [('state', '=', 'draft'), ('date', '<=', date_to)]
    #         options['unposted_in_period'] = bool(self.env['account.move'].search_count(period_domain))
    #
    #     if options.get('journals'):
    #         journals_selected = set(journal['id'] for journal in options['journals'] if journal.get('selected'))
    #         for journal_group in self.env['account.journal.group'].search([('company_id', '=', self.env.company.id)]):
    #             if journals_selected and journals_selected == set(self._get_filter_journals().ids) - set(journal_group.excluded_journal_ids.ids):
    #                 options['name_journal_group'] = journal_group.name
    #                 break
    #
    #     report_manager = self._get_report_manager(options)
    #     info = {'options': options,
    #             'context': self.env.context,
    #             'report_manager_id': report_manager.id,
    #             'footnotes': [{'id': f.id, 'line': f.line, 'text': f.text} for f in report_manager.footnotes_ids],
    #             'buttons': self._get_reports_buttons_in_sequence(options),
    #             'main_html': self.get_html(options),
    #             'searchview_html': self.env['ir.ui.view']._render_template(self._get_templates().get('search_template', 'account_report.search_template'), values=searchview_dict),
    #             }
    #     return info

