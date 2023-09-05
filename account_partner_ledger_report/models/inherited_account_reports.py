# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    # filter_currency_2 = None
    # filter_currency = [{'id':1, 'name': 'EUR', 'selected': False},{'id':2, 'name': 'USD', 'selected': False},{'id':74, 'name': 'EGP', 'selected': False},{'id':142, 'name': 'GBP', 'selected': False},]
    
    # def get_report_informations(self, options):
    #     '''
    #     return a dictionary of informations that will be needed by the js widget, manager_id, footnotes, html of report and searchview, ...
    #     '''
    #     options = self._get_options(options)
    #     self = self.with_context(self._set_context(options)) # For multicompany, when allowed companies are changed by options (such as aggregare_tax_unit)

    #     searchview_dict = {'options': options, 'context': self.env.context}
    #     # Check if report needs analytic
    #     if options.get('analytic_accounts') is not None:
    #         options['selected_analytic_account_names'] = [self.env['account.analytic.account'].browse(int(account)).name for account in options['analytic_accounts']]
    #     # if options.get('currency_id') is not None:
    #     #     selected_currency_id = self.env['res.currency'].search([('id', '=', currency_id)],limit = 1)
    #     #     options['selected_currency_name'] = selected_currency_id.name or ''
    #     if options.get('analytic_tags') is not None:
    #         options['selected_analytic_tag_names'] = [self.env['account.analytic.tag'].browse(int(tag)).name for tag in options['analytic_tags']]
    #     if options.get('partner'):
    #         options['selected_partner_ids'] = [self.env['res.partner'].browse(int(partner)).name for partner in options['partner_ids']]
    #         options['selected_partner_categories'] = [self.env['res.partner.category'].browse(int(category)).name for category in (options.get('partner_categories') or [])]

    #     # Check whether there are unposted entries for the selected period or not (if the report allows it)
    #     if options.get('date') and options.get('all_entries') is not None:
    #         date_to = options['date'].get('date_to') or options['date'].get('date') or fields.Date.today()
    #         period_domain = [('state', '=', 'draft'), ('date', '<=', date_to)]
    #         options['unposted_in_period'] = bool(self.env['account.move'].search_count(period_domain))

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

    # def _init_filter_currency(self, options, previous_options=None):
    #     # if not self.filter_analytic:
    #     #     return
    #     # options['currency'] = self.filter_currency
        
    #     options['currency_active'] = True
    #     currency_id = 1
    #     for c in  options.get('currency',[]):
    #         if c['selected']:
    #             currency_id = c['id']
    #     selected_currency_id = self.env['res.currency'].search([('id', '=', currency_id)],limit = 1)
    #     options['currency_id'] = selected_currency_id.id or  0
    #     options['all_currency_ids'] = self.env['res.currency'].search([])
    #     options['selected_currency_name'] = selected_currency_id.name or False



