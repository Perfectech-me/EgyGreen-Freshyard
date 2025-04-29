from odoo import api, models, fields
from odoo.exceptions import ValidationError

class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    has_confirmation_bill_group = fields.Boolean(compute='_compute_has_confirmation_bill_group')

    def _compute_has_confirmation_bill_group(self):
        for record in self:
            record.has_confirmation_bill_group = self.env.user.has_group(
                'Budget_validation.confirmation_bill_button_group')

    def _check_budget_range(self):
        for rec in self:
            for line in rec.invoice_line_ids:
                budgets = self.env['crossovered.budget.lines'].search([
                    ('analytic_account_id', '=', line.analytic_account_id.id),
                ])
                for budget in budgets:
                    if line.price_unit > budget.planned_amount:
                        raise ValidationError(
                            f"Line '{line.name}': price {line.price_unit} exceeds budget limit {budget.planned_amount}"
                        )


    def action_post_access(self):
        return super(AccountMoveInh, self).action_post()

    def action_post(self):
        self._check_budget_range()
        return super(AccountMoveInh, self).action_post()
