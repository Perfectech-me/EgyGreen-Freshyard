from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import  timedelta
from odoo.tools import float_is_zero
from odoo.exceptions import ValidationError
class report_account_partner_ledger(models.Model):
    _inherit = "account.move.line"
    def get_matching_number(self):
        name = ','.join(self.matched_debit_ids.mapped('debit_move_id.move_id.name') + self.matched_credit_ids.mapped('credit_move_id.move_id.name') )
        return name
