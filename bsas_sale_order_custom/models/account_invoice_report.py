from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    invoice_person_user_id = fields.Many2one(comodel_name="sales.person.users",
                                             string="Sales Person")
    _depends = {'account.move': ['invoice_person_user_id'],}

    def _select(self):
        return super()._select() + ", move.invoice_person_user_id"
