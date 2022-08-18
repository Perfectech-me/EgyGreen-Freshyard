from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import timedelta, datetime
class account_move_report_wizard(models.Model):
    _name = 'cheque.wizard'
    _description = 'Cheque Wizard'

    payer_user_id = fields.Many2one(comodel_name="res.partner", string="Payer", required=False, )
    payee_user_id = fields.Many2one(comodel_name="res.partner", string="Payee", required=False, )
    from_date = fields.Date(string="From", required=True, )
    to_date = fields.Date(string="To", required=True, )
    status = fields.Selection(string="",
                              selection=[('draft', 'Draft'), ('registered', 'Registered'), ('bank', 'Bank Repository'),
                                         ('bounced', 'Bounced'),
                                         ('done', 'Done'), ('cancel', 'Cancel'), ], required=False)
    type = fields.Selection(string="", selection=[('incoming', 'incoming'), ('outgoing', 'outgoing'), ],
                            required=True )

    # @api.multi
    def get_today(self):
        return datetime.today().date()
    # @api.multi
    def if_status(self):
        if self.status:
            return True

    # @api.multi
    def generate_cheque_report(self):
        domain=[]
        if self.from_date > self.to_date:
            raise ValidationError('تاريخ البدأ أكبر من تاريخ النتهاء')
        domain.append (('cheque_date', '>=', self.from_date))
        domain.append(('cheque_date', '<=', self.to_date))
        if self.payer_user_id:
            domain.append(('payer_user_id', '=', self.payer_user_id.id))
        if self.status:
            domain.append(('status', '=', self.status))
        if self.payee_user_id:
            domain.append(('payee_user_id', '=', self.payee_user_id.id))
        domain.append(('type', '=', self.type))
        print(domain)
        return self.env['account.cheque'].search(domain)

    # @api.multi
    def incoming_report_method(self):
        return self.env.ref('account_cheque.incoming_report_get').report_action(self)

    # @api.multi
    def outgoing_report_method(self):
        return self.env.ref('account_cheque.outgoing_report_get').report_action(self)

    def outgoing_print_method(self):
        return self.env.ref('account_cheque.print_get').report_action(self)

