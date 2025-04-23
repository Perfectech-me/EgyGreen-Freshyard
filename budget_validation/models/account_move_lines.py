from odoo import api, models, fields
from odoo.exceptions import ValidationError

class AccountMoveLineInh(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('price_unit', 'analytic_account_id')
    def _check_line_budget(self):
        for line in self:
            if line.analytic_account_id:
                budgets = self.env['crossovered.budget.lines'].search([
                    ('analytic_account_id', '=', line.analytic_account_id.id),
                ])
                for budget in budgets:
                    if line.price_unit > budget.planned_amount:
                        raise ValidationError(
                            f"Line '{line.name}': price {line.price_unit} exceeds budget limit {budget.planned_amount}"
                        )