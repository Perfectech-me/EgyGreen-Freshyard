from odoo import api, models, fields
from odoo.exceptions import ValidationError

class AccountMoveInh(models.Model):
    _inherit = 'account.move'

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

    def action_post(self):
        self._check_budget_range()
        return super(AccountMoveInh, self).action_post()

