from odoo import models, fields, api,_
from datetime import datetime,date,timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


#
# class SaleAdvancePaymentInv(models.TransientModel):
#     _inherit = "sale.advance.payment.inv"
#     _description = "Sales Advance Payment Invoice"
#
#     def create_invoices(self):
#         sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
#
#         if self.advance_payment_method == 'delivered':
#             sale_orders._create_invoices(final=self.deduct_down_payments)
#         else:
#             # Create deposit product if necessary
#             if not self.product_id:
#                 vals = self._prepare_deposit_product()
#                 self.product_id = self.env['product.product'].create(vals)
#                 self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)
#
#             sale_line_obj = self.env['sale.order.line']
#             for order in sale_orders:
#                 amount, name = self._get_advance_details(order)
#
#                 if self.product_id.invoice_policy != 'order':
#                     raise UserError(
#                         _('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
#                 if self.product_id.type != 'service':
#                     raise UserError(
#                         _("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
#                 taxes = self.product_id.taxes_id.filtered(
#                     lambda r: not order.company_id or r.company_id == order.company_id)
#                 tax_ids = order.fiscal_position_id.map_tax(taxes).ids
#                 analytic_tag_ids = []
#                 for line in order.order_line:
#                     analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
#
#                 so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
#                 so_line = sale_line_obj.create(so_line_values)
#                 print("analytic",analytic_tag_ids)
#                 for so in so_line:
#                     for s in so.line_ids:
#                         s.analytic_tag_ids=analytic_tag_ids
#                 self._create_invoice(order, so_line, amount)
#         if self._context.get('open_invoices', False):
#             return sale_orders.action_view_invoice()
#         return {'type': 'ir.actions.act_window_close'}
#
#         return super(SaleAdvancePaymentInv, self).create_invoices()

class AccountMove(models.Model):
    _inherit='account.move'
    @api.model_create_multi
    def create(self, vals_list):
        print("ssss",self,vals_list)
        # OVERRIDE
        analytic_tag_ids=[]
        analytic_ids=0
        res=super(AccountMove, self).create(vals_list)
        for r in res.line_ids:
            if r.analytic_tag_ids:
                analytic_tag_ids=r.analytic_tag_ids
            else:
                r.analytic_tag_ids=analytic_tag_ids

            print("rrr",r.analytic_tag_ids)
            for n in r.analytic_tag_ids:
                print("n.",n.analytic_distribution_ids)

                for s in n.analytic_distribution_ids:
                    analytic_ids=s['account_id'].id
                    print("sssss",s['account_id'].id)
                # selected_analytic_tags = self.env['account.analytic.tag'].search([('id', 'in', analytic_tag_ids)])
            if r.analytic_account_id:
                analytic_tag_ids = r.analytic_tag_ids
            else:
                r.analytic_account_id = analytic_ids

                # for s in selected_analytic_tags.account_id:
                #     print("")

        return res



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def set_analytic_tag(self):
        if not self.analytic_account_id.id:
            raise ValidationError(
                _("Please Insert Analytic Account")
            )

        analytic_tag=self.env['account.analytic.tag'].sudo().create(
            {'name': self.name, 'active_analytic_distribution': True, 'company_id': self.company_id.id,
             'analytic_distribution_ids': [(0, 0, {'account_id': self.analytic_account_id.id, 'percentage': 1.0})]})
        for rec in self:
            print('rec.analytic_account_id.id',rec.analytic_account_id.name)
            for par in rec.order_line:
                if par.analytic_tag_ids:
                     analytic_tag=par.analytic_tag_ids



            for par in rec.order_line:
                if not par.analytic_tag_ids:
                   par.analytic_tag_ids=analytic_tag



