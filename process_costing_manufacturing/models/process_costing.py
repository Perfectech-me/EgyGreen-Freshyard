from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
import math
from odoo.tools import float_is_zero, float_round


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_overhead_cost = fields.Boolean(default=False)
    is_labor_cost = fields.Boolean(default=False)
    work_in_progress = fields.Many2one('account.account')


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        for material in res.bom_line_ids:
            product_id = self.env['product.template'].search([('name', '=', material.product_id.name)])
            vals = {
                'product_id': product_id.id,
                'planned_qty': material.product_qty,
                'uom_id': material.product_uom_id.id,
                'cost': material.product_id.standard_price,
                'mrp_bom_material_id': res.id,
            }
            material_obj = self.env['mrp.bom.material.cost'].create(vals)
        return res

        # bom_material_cost_ids = fields.One2many("mrp.bom.material.cost","mrp_bom_material_id","Material Cost")

    bom_labour_cost_ids = fields.One2many("mrp.bom.labour.cost", "mrp_bom_labour_id", "labour cost")
    bom_overhead_cost_ids = fields.One2many("mrp.bom.overhead.cost", "mrp_bom_overhead_id", "overhead cost")
    # single page total cost
    # bom_total_material_cost = fields.Float(compute='_compute_total_cost',string="Total Material Cost",default=0.0)
    bom_total_labour_cost = fields.Float(compute='_compute_total_cost', string="Total Labour Cost", default=0.0)
    bom_total_overhead_cost = fields.Float(compute='_compute_total_cost', string="Total Overhead Cost", default=0.0)
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

    def _compute_total_cost(self):
        # material_total = 0.0
        labour_total = 0.0
        overhead_total = 0.0

        # for line in self.bom_material_cost_ids:
        #     material_total += line.total_cost

        for line in self.bom_labour_cost_ids:
            labour_total += line.total_cost

        for line in self.bom_overhead_cost_ids:
            overhead_total += line.total_cost

        # self.bom_total_material_cost = material_total
        self.bom_total_labour_cost = labour_total
        self.bom_total_overhead_cost = overhead_total

        # @api.multi


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # @api.multi
    def write(self, vals):
        if vals.get('product_id'):
            product = self.env['product.product'].browse(vals.get('product_id'))
            old_product = self.env['product.template'].search([('name', '=', self.product_id.name)])
            product_id = self.env['product.template'].search([('name', '=', product.name)])

            material_product_id = self.env['mrp.bom.material.cost'].search(
                [('product_id', '=', old_product.id), ('mrp_bom_material_id', '=', self.bom_id.id)])
            material_vals = {
                'product_id': product_id.id,
                'uom_id': product_id.uom_id.id,
                'cost': product_id.standard_price,
                'planned_qty': self.product_qty or vals.get('product_qty'),
            }
            material_product_id.write(material_vals)

        if vals.get('product_qty'):
            product = self.env['product.product'].browse(self.product_id)
            product_id = self.env['product.template'].search([('name', '=', self.product_id.name)])
            material_product_id = self.env['mrp.bom.material.cost'].search(
                [('product_id', '=', product_id.id), ('mrp_bom_material_id', '=', self.bom_id.id)])
            material_product_id.write({'planned_qty': vals.get('product_qty')})

        res = super(MrpBomLine, self).write(vals)
        return res


class MrpBomMaterialCost(models.Model):
    _name = "mrp.bom.material.cost"

    operation_id = fields.Many2one('mrp.routing.workcenter', string="Operation")
    product_id = fields.Many2one('product.template', string="Product")
    planned_qty = fields.Float(string="Planned Qty", default=0.0)
    actual_qty = fields.Float(string="Actual Qty", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="UOM")
    cost = fields.Float(string="Cost/Unit")
    total_cost = fields.Float(compute='onchange_planned_qty', string="Total Cost")
    total_actual_cost = fields.Float(compute='onchange_planned_qty', string="Total Actual Cost")
    mrp_bom_material_id = fields.Many2one("mrp.bom", "Mrp Bom Material")
    mrp_pro_material_id = fields.Many2one("mrp.production", "Mrp Production Material")
    mrp_wo_material_id = fields.Many2one("mrp.workorder", "Mrp Workorder Material")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

    # @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

    # @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        self.cost = self.product_id.standard_price

    @api.onchange('planned_qty', 'cost')
    def onchange_planned_qty(self):
        for line in self:
            price = line.planned_qty * line.cost
            actual_price = line.actual_qty * line.cost
            line.total_cost = price
            line.total_actual_cost = actual_price


class MrpBomLabourCost(models.Model):
    _name = "mrp.bom.labour.cost"

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        self.cost = self.product_id.standard_price

    @api.onchange('planned_qty', 'cost')
    def onchange_labour_planned_qty(self):
        for line in self:
            price = line.planned_qty * line.cost
            actual_price = line.actual_qty * line.cost
            line.total_cost = price
            line.total_actual_cost = actual_price

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

    operation_id = fields.Many2one('mrp.routing.workcenter', string="Operation")
    product_id = fields.Many2one('product.template', string="Product")
    planned_qty = fields.Float(string="Planned Qty", default=0.0)
    actual_qty = fields.Float(string="Actual Qty", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="UOM")
    cost = fields.Float(string="Cost/Unit")
    total_cost = fields.Float(compute='onchange_labour_planned_qty', string="Total Cost")
    total_actual_cost = fields.Float(compute='onchange_labour_planned_qty', string="Total Actual Cost")
    # total_labour_cost = fields.Float(string="Total Labour Cost")
    mrp_bom_labour_id = fields.Many2one("mrp.bom", "Mrp Bom Labour")
    mrp_pro_labour_id = fields.Many2one("mrp.production", "Mrp Production Labour")
    mrp_wo_labour_id = fields.Many2one("mrp.workorder", "Mrp Workorder Labour")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")


class MrpBomOverheadCost(models.Model):
    _name = "mrp.bom.overhead.cost"

    # @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        if not self.product_id:
            return res
        self.uom_id = self.product_id.uom_id.id
        self.cost = self.product_id.standard_price

    # @api.multi
    @api.onchange('planned_qty', 'cost')
    def onchange_overhead_planned_qty(self):
        for line in self:
            price = line.planned_qty * line.cost
            actual_price = line.actual_qty * line.cost
            line.total_cost = price
            line.total_actual_cost = actual_price

    # @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

    operation_id = fields.Many2one('mrp.routing.workcenter', string="Operation")
    product_id = fields.Many2one('product.template', string="Product")
    planned_qty = fields.Float(string="Planned Qty", default=0.0)
    actual_qty = fields.Float(string="Actual Qty", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="UOM")
    cost = fields.Float(string="Cost/Unit")
    total_cost = fields.Float(compute='onchange_overhead_planned_qty', string="Total Cost")
    total_actual_cost = fields.Float(compute='onchange_overhead_planned_qty', string="Total Actual Cost")
    # total_overhead_cost = fields.Float(string="Total Overhead Cost")
    mrp_bom_overhead_id = fields.Many2one("mrp.bom", "Mrp Bom Overhead")
    mrp_pro_overhead_id = fields.Many2one("mrp.production", "Mrp Production Overhead")
    mrp_wo_overhead_id = fields.Many2one("mrp.workorder", "Mrp Workorder Overhead")
    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    origin_id = fields.Many2one(
        'account.analytic.tag',
        string='Source',
        copy=False,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Reference of the document that generated this production order request."
    )

    def _create_journal_entries(self):
        self.ensure_one()
        today = fields.Datetime.now()
        labor_journal = self.env['account.journal'].search([('is_labor_cost', '=', True)], limit=1)
        over_journal = self.env['account.journal'].search([('is_overhead_cost', '=', True)], limit=1)
        if self.qty_producing != 0:
            name = self.name + " - " + self.product_id.name
            account_move = self.env['account.move'].search([('ref', 'ilike', name)])

            if self.pro_labour_cost_ids:
                move = self.env['account.move'].create({
                    'move_type': 'entry',
                    'date': today,
                    'journal_id': labor_journal.id,
                    'ref': str(self.name) + " - Labour Cost"
                })
                total_line = 0
                credit_1 = []
                for line in self.pro_labour_cost_ids:
                    expense_account_id = line.product_id.property_account_expense_id.id
                    total_line += line.total_actual_cost
                    credit_1.append((0, 0, {'move_id': move.id,
                                            'account_id': expense_account_id,
                                            'date': today,
                                            'currency_id': self.currency_id.id,
                                            'credit': line.total_actual_cost,
                                            'debit': 0.0,
                                            'name': str(self.name) + " - Labour Cost",
                                            }
                                     ))

                credit_1.append((0, 0, {'move_id': move.id,
                                        'account_id': labor_journal.work_in_progress.id,
                                        'date': today,
                                        'currency_id': self.currency_id.id,
                                        'credit': 0.0,
                                        'debit': total_line,
                                        }))
                move.write({'line_ids': credit_1})
                move.action_post()

            # for line in self.pro_overhead_cost_ids:
            if self.pro_overhead_cost_ids:
                move = self.env['account.move'].create({
                    'move_type': 'entry',
                    'date': today,
                    'journal_id': over_journal.id,
                    'ref': str(self.name) + " - Overheads Cost"
                })
                total_line = 0
                credit_1 = []
                for line in self.pro_overhead_cost_ids:
                    expense_account_id = line.product_id.property_account_expense_id.id
                    total_line += line.total_actual_cost
                    credit_1.append((0, 0, {'move_id': move.id,
                                            'account_id': expense_account_id,
                                            'date': today,
                                            'currency_id': self.currency_id.id,
                                            'credit': line.total_actual_cost,
                                            'debit': 0.0,
                                            'name': str(self.name) + " - Overheads Cost",
                                           }
                                     ))

                credit_1.append((0, 0, {'move_id': move.id,
                                        'account_id': over_journal.work_in_progress.id,
                                        'date': today,
                                        'currency_id': self.currency_id.id,
                                        'credit': 0.0,
                                        'debit': total_line,
                                        }))
                move.write({'line_ids': credit_1})
                move.action_post()

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for order in self:
            order._create_journal_entries()
        return res

    def action_view_mrp_production_childs(self):
        self.ensure_one()
        mrp_production_ids = self._get_children().ids
        action = {
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
        }
        if len(mrp_production_ids) == 1:
            child_production = self.env['mrp.production'].browse(mrp_production_ids[0])
            product_ids = child_production.mapped('product_id')  # Get unique product IDs from child MOs
            if product_ids:
                bom_id = self.env['mrp.bom'].search([('product_tmpl_id.product_variant_ids', 'in', product_ids.ids)],
                                                    limit=1)
                action.update({
                    'view_mode': 'form',
                    'res_id': mrp_production_ids[0],
                })
                if bom_id:
                    child_production.write({'bom_id': bom_id.id})
            else:
                action.update({
                    'name': _("No Child MO's found for %s") % self.name,
                    'view_mode': 'tree',
                    'view_type': 'form',
                    'target': 'new',
                })
        else:
            action.update({
                'name': _("Child MO's for %s") % self.name,
                'domain': [('id', 'in', mrp_production_ids)],
                'view_mode': 'tree,form',
            })
        return action

    def _generate_workorders(self, exploded_boms):
        workorders = self.env['mrp.workorder']
        list_of_material = []
        list_of_labour = []
        list_of_overhead = []

        # for material in self.pro_material_cost_ids:
        #     list_of_material.append(material.id)

        for labour in self.pro_labour_cost_ids:
            list_of_labour.append(labour.id)

        for overhead in self.pro_overhead_cost_ids:
            list_of_overhead.append(overhead.id)

        for bom, bom_data in exploded_boms:
            if bom.routing_id.id and (
                    not bom_data['parent_line'] or bom_data['parent_line'].bom_id.routing_id.id != bom.routing_id.id):
                workorders += self._workorders_create(bom, bom_data)
                workorders.write({'wo_labour_cost_ids': [(6, 0, list_of_labour)],
                                  'wo_overhead_cost_ids': [(6, 0, list_of_overhead)], })
        return workorders

    @api.depends('product_id')
    def _get_lines_po(self):
        for rec in self:
            list_of_labour = []
            list_of_overhead = []
            if rec.product_id:
                bom = self.env['mrp.bom']._bom_find(self.product_id)[self.product_id]
                for b in bom:
                    if b:
                        if b.type == 'normal':
                            # self.bom_id = b.id
                            for labour in b.bom_labour_cost_ids:
                                list_of_labour.append(labour.id)
                            self.pro_labour_cost_ids = [(6, 0, list_of_labour)]
                            for overhead in b.bom_overhead_cost_ids:
                                list_of_overhead.append(overhead.id)
                            self.pro_overhead_cost_ids = [(6, 0, list_of_overhead)]

    def _compute_total_cost(self):
        material_total = 0.0
        material_actual_total = 0.0

        labour_total = 0.0
        labour_actual_total = 0.0

        overhead_total = 0.0
        overhead_actual_total = 0.0

        for line in self.pro_labour_cost_ids:
            labour_total += line.total_cost
            labour_actual_total += line.total_actual_cost

        for line in self.pro_overhead_cost_ids:
            overhead_total += line.total_cost
            overhead_actual_total += line.total_actual_cost

        self.total_material_cost = 0.0
        for line in self.move_raw_ids:
            print('*********** product_id.name', line.product_id.name)
            print('*********** product_id.standard_price', line.product_id.standard_price)
            print('*********** quantity_done', line.quantity_done)

            self.total_material_cost += line.product_id.standard_price * line.quantity_done
            print('#### total_material_cost', self.total_material_cost)

        # self.total_material_cost = material_total
        self.total_actual_material_cost = self.total_material_cost

        self.total_labour_cost = labour_total
        self.total_actual_labour_cost = labour_actual_total

        self.total_overhead_cost = overhead_total
        self.total_actual_overhead_cost = overhead_actual_total

    def _compute_total_all_cost(self):
        total = 0.0
        actual_total = 0.0
        total = self.total_material_cost + self.total_labour_cost + self.total_overhead_cost
        actual_total = self.total_actual_material_cost + self.total_actual_labour_cost + self.total_actual_overhead_cost
        self.total_all_cost = total
        self.total_actual_all_cost = actual_total

    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

    def _compute_total_product_cost(self):
        total = 0.0
        for line in self.finished_move_line_ids:
            if line.qty_done != 0.0:
                total = self.total_actual_all_cost / line.qty_done
        self.product_unit_cost = total

    def _cal_price(self, consumed_moves):
        super(MrpProduction, self)._cal_price(consumed_moves)
        work_center_cost = 0
        finished_move = self.move_finished_ids.filtered(
            lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel') and x.quantity_done > 0)
        if finished_move:
            finished_move.ensure_one()
            for work_order in self.workorder_ids:
                time_lines = work_order.time_ids.filtered(
                    lambda x: x.date_end and not x.cost_already_recorded)
                duration = sum(time_lines.mapped('duration'))
                time_lines.write({'cost_already_recorded': True})
                work_center_cost += (duration / 60.0) * \
                    work_order.workcenter_id.costs_hour
            qty_done = finished_move.product_uom._compute_quantity(
                finished_move.quantity_done, finished_move.product_id.uom_id)
            extra_cost = self.extra_cost * qty_done
            labour_cost = self.total_actual_labour_cost or 0
            over_head_cost = self.total_actual_overhead_cost or 0
            print(extra_cost)
            extra_cost += labour_cost + over_head_cost
            total_cost = (sum(-m.stock_valuation_layer_ids.value for m in consumed_moves.sudo()) + work_center_cost + extra_cost)
            byproduct_moves = self.move_byproduct_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.quantity_done > 0)
            byproduct_cost_share = 0
            for byproduct in byproduct_moves:
                if byproduct.cost_share == 0:
                    continue
                byproduct_cost_share += byproduct.cost_share
                if byproduct.product_id.cost_method in ('fifo', 'average'):
                    byproduct.price_unit = total_cost * byproduct.cost_share / 100 / byproduct.product_uom._compute_quantity(byproduct.quantity_done, byproduct.product_id.uom_id)
            if finished_move.product_id.cost_method in ('fifo', 'average'):
                finished_move.price_unit = total_cost * float_round(1 - byproduct_cost_share / 100, precision_rounding=0.0001) / qty_done
        return True


    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

    precent = fields.Float(string="Precent", required=False, )
    pro_labour_cost_ids = fields.One2many("mrp.bom.labour.cost", "mrp_pro_labour_id", "Labour Cost",
                                          compute="_get_lines_po", readonly=False)
    pro_overhead_cost_ids = fields.One2many("mrp.bom.overhead.cost", "mrp_pro_overhead_id", "Overhead Cost",
                                            compute="_get_lines_po", readonly=False)
    pro_total_material_cost = fields.Float(string="Total Material Cost", default=0.0)

    total_material_cost = fields.Float(compute='_compute_total_cost', string="Total Material Cost", default=0.0)
    total_labour_cost = fields.Float(compute='_compute_total_cost', string="Total Labour Cost", default=0.0)
    total_overhead_cost = fields.Float(compute='_compute_total_cost', string="Total Overhead Cost", default=0.0)
    total_all_cost = fields.Float(compute='_compute_total_all_cost', string="Total Cost", default=0.0)

    total_actual_material_cost = fields.Float(compute='_compute_total_cost',readonly=False, string="Total Actual Material Cost",
                                              default=0.0)
    total_actual_labour_cost = fields.Float(compute='_compute_total_cost', string="Total Actual Labour Cost",
                                            default=0.0)
    total_actual_overhead_cost = fields.Float(compute='_compute_total_cost', string="Total Actual Overhead Cost",
                                              default=0.0)
    total_actual_all_cost = fields.Float(compute='_compute_total_all_cost', string="Total Actual Cost", default=0.0)

    product_unit_cost = fields.Float(compute='_compute_total_product_cost', string="Product Unit Cost", default=0.0)


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def _compute_total_cost(self):
        material_total = 0.0
        material_actual_total = 0.0

        labour_total = 0.0
        labour_actual_total = 0.0

        overhead_total = 0.0
        overhead_actual_total = 0.0

        for order in self:
            # for line in order.wo_material_cost_ids:
            #     material_total += line.total_cost
            #     material_actual_total += line.total_actual_cost
            order.total_material_cost = 0
            order.total_actual_material_cost = 0

            for line in order.wo_labour_cost_ids:
                labour_total += line.total_cost
                labour_actual_total += line.total_actual_cost
            order.total_labour_cost = labour_total
            order.total_actual_labour_cost = labour_actual_total

            for line in order.wo_overhead_cost_ids:
                overhead_total += line.total_cost
                overhead_actual_total += line.total_actual_cost
            order.total_overhead_cost = overhead_total
            order.total_actual_overhead_cost = overhead_actual_total

    def _compute_total_all_cost(self):
        total = 0.0
        actual_total = 0.0
        for line in self:
            total = line.total_material_cost + line.total_labour_cost + line.total_overhead_cost
            actual_total = line.total_actual_material_cost + line.total_actual_labour_cost + line.total_actual_overhead_cost
            line.total_all_cost = total
            line.total_actual_all_cost = actual_total

    # @api.multi
    def get_currency_id(self):
        user_id = self.env.uid
        res_user_id = self.env['res.users'].browse(user_id)
        for line in self:
            line.currency_id = res_user_id.company_id.currency_id

    # @api.depends('total_all_cost')
    # def check_precent(self):
    #     for rec in self:
    #
    #          rec.precent = rec.total_all_cost * (.95)
    #
    # @api.depends('precent')
    # def check_cost_product(self):
    #     for rec in self:
    #
    #          rec.cost1 = rec.precent / rec.product_qty

    currency_id = fields.Many2one("res.currency", compute='get_currency_id', string="Currency")

    # wo_material_cost_ids = fields.One2many("mrp.bom.material.cost","mrp_wo_material_id","Material Cost")

    wo_labour_cost_ids = fields.One2many("mrp.bom.labour.cost", "mrp_wo_labour_id", "Labour Cost", )
    wo_overhead_cost_ids = fields.One2many("mrp.bom.overhead.cost", "mrp_wo_overhead_id", "Overhead Cost")
    # wo_total_material_cost = fields.Float(string="Total Material Cost",default=0.0)

    # Costing Tab
    total_material_cost = fields.Float(compute='_compute_total_cost', string="Total Material Cost", default=0.0)
    total_labour_cost = fields.Float(compute='_compute_total_cost', string="Total Labour Cost", default=0.0)
    total_overhead_cost = fields.Float(compute='_compute_total_cost', string="Total Overhead Cost", default=0.0)
    total_all_cost = fields.Float(compute='_compute_total_all_cost', string="Total Cost", default=0.0)
    precent = fields.Float(string="Precent", compute='check_precent', required=False, )
    # cost1 = fields.Float(string="product cost", compute = 'check_cost_product', required=False, )
    # Costing Tab
    total_actual_material_cost = fields.Float(compute='_compute_total_cost', string="Total Actual Material Cost",
                                              default=0.0)
    total_actual_labour_cost = fields.Float(compute='_compute_total_cost', string="Total Actual Labour Cost",
                                            default=0.0)
    total_actual_overhead_cost = fields.Float(compute='_compute_total_cost', string="Total Actual Overhead Cost",
                                              default=0.0)
    total_actual_all_cost = fields.Float(compute='_compute_total_all_cost', string="Total Actual Cost", default=0.0)

    product_unit_cost = fields.Float(string="Product Unit Cost", default=0.0)


class ChangeProductionQty(models.TransientModel):
    _inherit = 'change.production.qty'

    # @api.multi
    # def change_prod_qty(self):
    #     precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #     for wizard in self:
    #         production = wizard.mo_id
    #         produced = sum(production.move_finished_ids.filtered(lambda m: m.product_id == production.product_id).mapped('quantity_done'))
    #         if wizard.product_qty < produced:
    #             format_qty = '%.{precision}f'.format(precision=precision)
    #             raise UserError(_("You have already processed %s. Please input a quantity higher than %s ") % (format_qty % produced, format_qty % produced))
    #         old_production_qty = production.product_qty
    #         production.write({'product_qty': wizard.product_qty})
    #
    #         # Change Material,Labour and Overhead quantity
    #         # for material in production.pro_material_cost_ids:
    #         #     for bom in production.bom_id.bom_line_ids:
    #         #         if material.product_id.id == bom.product_id.id:
    #         #             material.write({'planned_qty':wizard.product_qty*bom.product_qty,'actual_qty':wizard.product_qty*bom.product_qty})
    #
    #         for labour in production.pro_labour_cost_ids:
    #             for bom in production.bom_id.bom_labour_cost_ids:
    #                 if labour.product_id.id == bom.product_id.id:
    #                     labour.write({'planned_qty':wizard.product_qty*bom.planned_qty,'actual_qty':wizard.product_qty*bom.planned_qty})
    #
    #         for overhead in production.pro_overhead_cost_ids:
    #             for bom in production.bom_id.bom_overhead_cost_ids:
    #                 if overhead.product_id.id == bom.product_id.id:
    #                     overhead.write({'planned_qty':wizard.product_qty*bom.planned_qty,'actual_qty':wizard.product_qty*bom.planned_qty})
    #
    #         done_moves = production.move_finished_ids.filtered(lambda x: x.state == 'done' and x.product_id == production.product_id)
    #         qty_produced = production.product_id.uom_id._compute_quantity(sum(done_moves.mapped('product_qty')), production.product_uom_id)
    #         factor = production.product_uom_id._compute_quantity(production.product_qty - qty_produced, production.bom_id.product_uom_id) / production.bom_id.product_qty
    #         boms, lines = production.bom_id.explode(production.product_id, factor, picking_type=production.bom_id.picking_type_id)
    #         documents = {}
    #         for line, line_data in lines:
    #             move, old_qty, new_qty = production._update_raw_move(line, line_data)
    #             iterate_key = production._get_document_iterate_key(move)
    #             if iterate_key:
    #                 document = self.env['stock.picking']._log_activity_get_documents({move: (new_qty, old_qty)}, iterate_key, 'UP')
    #                 for key, value in document.items():
    #                     if documents.get(key):
    #                         documents[key] += [value]
    #                     else:
    #                         documents[key] = [value]
    #         production._log_manufacture_exception(documents)
    #         operation_bom_qty = {}
    #         for bom, bom_data in boms:
    #             for operation in bom.routing_id.operation_ids:
    #                 operation_bom_qty[operation.id] = bom_data['qty']
    #         finished_moves_modification = self._update_product_to_produce(production, production.product_qty - qty_produced, old_production_qty)
    #         production._log_downside_manufactured_quantity(finished_moves_modification)
    #         moves = production.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
    #         moves._action_assign()
    #         for wo in production.workorder_ids:
    #             operation = wo.operation_id
    #             if operation_bom_qty.get(operation.id):
    #                 cycle_number = float_round(operation_bom_qty[operation.id] / operation.workcenter_id.capacity, precision_digits=0, rounding_method='UP')
    #                 wo.duration_expected = (operation.workcenter_id.time_start +
    #                              operation.workcenter_id.time_stop +
    #                              cycle_number * operation.time_cycle * 100.0 / operation.workcenter_id.time_efficiency)
    #             quantity = wo.qty_production - wo.qty_produced
    #             if production.product_id.tracking == 'serial':
    #                 quantity = 1.0 if not float_is_zero(quantity, precision_digits=precision) else 0.0
    #             else:
    #                 quantity = quantity if (quantity > 0) else 0
    #             if float_is_zero(quantity, precision_digits=precision):
    #                 wo.final_lot_id = False
    #                 wo.active_move_line_ids.unlink()
    #             wo.qty_producing = quantity
    #             if wo.qty_produced < wo.qty_production and wo.state == 'done':
    #                 wo.state = 'progress'
    #             if wo.qty_produced == wo.qty_production and wo.state == 'progress':
    #                 wo.state = 'done'
    #             # assign moves; last operation receive all unassigned moves
    #             # TODO: following could be put in a function as it is similar as code in _workorders_create
    #             # TODO: only needed when creating new moves
    #             moves_raw = production.move_raw_ids.filtered(lambda move: move.operation_id == operation and move.state not in ('done', 'cancel'))
    #             if wo == production.workorder_ids[-1]:
    #                 moves_raw |= production.move_raw_ids.filtered(lambda move: not move.operation_id)
    #             moves_finished = production.move_finished_ids.filtered(lambda move: move.operation_id == operation) #TODO: code does nothing, unless maybe by_products?
    #             moves_raw.mapped('move_line_ids').write({'workorder_id': wo.id})
    #             (moves_finished + moves_raw).write({'workorder_id': wo.id})
    #             if quantity > 0 and wo.move_raw_ids.filtered(lambda x: x.product_id.tracking != 'none') and not wo.active_move_line_ids:
    #                 wo._generate_lot_ids()
    #     return {}


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    def _compute_bom_price(self, bom, boms_to_recompute=False):
        self.ensure_one()
        if not bom:
            return 0
        if not boms_to_recompute:
            boms_to_recompute = []
        total = 0
        for opt in bom.operation_ids:
            duration_expected = (
                    opt.workcenter_id.time_start +
                    opt.workcenter_id.time_stop +
                    opt.time_cycle)
            total += (duration_expected / 60) * opt.workcenter_id.costs_hour
        for overhead in bom.bom_overhead_cost_ids:
            total += overhead.total_cost
            print("ana overhead llll", overhead.total_cost)
        for labour in bom.bom_labour_cost_ids:
            total += labour.total_cost
            print("ana labour llll", labour.total_cost)
        print("ana fe llll", total)
        for line in bom.bom_line_ids:
            if line._skip_bom_line(self):
                continue
            if line.child_bom_id and line.child_bom_id in boms_to_recompute:
                child_total = line.product_id._compute_bom_price(line.child_bom_id, boms_to_recompute=boms_to_recompute)
                total += line.product_id.uom_id._compute_price(child_total, line.product_uom_id) * line.product_qty
            else:
                total += line.product_id.uom_id._compute_price(line.product_id.standard_price,
                                                               line.product_uom_id) * line.product_qty
        return bom.product_uom_id._compute_price(total / bom.product_qty, self.uom_id)
