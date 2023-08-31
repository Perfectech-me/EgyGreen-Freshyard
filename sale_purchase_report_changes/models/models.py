# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api
class sale_purchase_report_changes(models.Model):
    _inherit = 'sale.report'
    order_category = fields.Selection(string="Order Catrgory", selection=[
                                                                            ('International', 'International'),
                                                                            ('Local', 'Local'),
                                                                            ('Export', 'Export'),
                                                                          ],default='International' )

    export_type = fields.Selection(string="Type", selection=[('fresh', 'Fresh'),('frozen','Frozen'), ('food_products', 'Food Products'),('other','Other') ],default='fresh')
    product_type = fields.Selection(string="Product Type", selection=[
        ('row_materials', 'Row Materials'),('sort','Sort'),('packing','Packing'), ('finish_products', 'Finish Products'),('other','Other') ],default='row_materials')

    def _select_sale(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as product_uom_qty,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_delivered / u.factor * u2.factor) ELSE 0 END as qty_delivered,
            CASE WHEN l.product_id IS NOT NULL THEN SUM((l.product_uom_qty - l.qty_delivered) / u.factor * u2.factor) ELSE 0 END as qty_to_deliver,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_invoiced / u.factor * u2.factor) ELSE 0 END as qty_invoiced,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_to_invoice / u.factor * u2.factor) ELSE 0 END as qty_to_invoice,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.price_total / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as price_total,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as price_subtotal,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as untaxed_amount_to_invoice,
            CASE WHEN l.product_id IS NOT NULL THEN sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as untaxed_amount_invoiced,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.company_id as company_id,
            s.campaign_id as campaign_id,
            s.medium_id as medium_id,
            s.source_id as source_id,
            extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.analytic_account_id as analytic_account_id,
            s.team_id as team_id,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.industry_id as industry_id,
            partner.commercial_partner_id as commercial_partner_id,
            CASE WHEN l.product_id IS NOT NULL THEN sum(p.weight * l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as weight,
            CASE WHEN l.product_id IS NOT NULL THEN sum(p.volume * l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as volume,
            l.discount as discount,
            CASE WHEN l.product_id IS NOT NULL THEN sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))ELSE 0 END as discount_amount,
            s.id as order_id,
            s.order_category as order_category,
            s.export_type as export_type,
            s.product_type as product_type
        """

        for field in fields.values():
            select_ += field
        return select_
    def _group_by_sale(self, groupby=''):
        groupby_ = """
            l.product_id,
            l.order_id,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.partner_id,
            s.user_id,
            s.state,
            s.company_id,
            s.campaign_id,
            s.medium_id,
            s.source_id,
            s.pricelist_id,
            s.analytic_account_id,
            s.team_id,
            p.product_tmpl_id,
            partner.country_id,
            partner.industry_id,
            partner.commercial_partner_id,
            l.discount,
            s.order_category,
            s.export_type,
            s.product_type,
            s.id %s
        """ % (groupby)
        return groupby_
class sale_purchase_report_changes(models.Model):
    _inherit = 'purchase.report'
    order_category = fields.Selection(string="Order Catrgory", selection=[
                                                                            ('International', 'International'),
                                                                            ('Local', 'Local'),
                                                                            ('Export', 'Export'),
                                                                          ],default='International' )

    export_type = fields.Selection(string="Type", selection=[('fresh', 'Fresh'),('frozen','Frozen'), ('food_products', 'Food Products'),('other','Other') ],default='fresh')
    product_type = fields.Selection(string="Product Type", selection=[
        ('row_materials', 'Row Materials'),('sort','Sort'),('packing','Packing'), ('finish_products', 'Finish Products'),('other','Other') ],default='row_materials')
    def _select(self):
        select_str = """
                SELECT
                    po.id as order_id,
                    min(l.id) as id,
                    po.date_order as date_order,
                    po.state,
                    po.date_approve,
                    po.dest_address_id,
                    po.partner_id as partner_id,
                    po.user_id as user_id,
                    po.company_id as company_id,
                    po.fiscal_position_id as fiscal_position_id,
                    l.product_id,
                    p.product_tmpl_id,
                    t.categ_id as category_id,
                    c.currency_id,
                    t.uom_id as product_uom,
                    extract(epoch from age(po.date_approve,po.date_order))/(24*60*60)::decimal(16,2) as delay,
                    extract(epoch from age(l.date_planned,po.date_order))/(24*60*60)::decimal(16,2) as delay_pass,
                    count(*) as nbr_lines,
                    sum(l.price_total / COALESCE(po.currency_rate, 1.0))::decimal(16,2) * currency_table.rate as price_total,
                    (sum(l.product_qty * l.price_unit / COALESCE(po.currency_rate, 1.0))/NULLIF(sum(l.product_qty/line_uom.factor*product_uom.factor),0.0))::decimal(16,2) * currency_table.rate as price_average,
                    partner.country_id as country_id,
                    partner.commercial_partner_id as commercial_partner_id,
                    analytic_account.id as account_analytic_id,
                    sum(p.weight * l.product_qty/line_uom.factor*product_uom.factor) as weight,
                    sum(p.volume * l.product_qty/line_uom.factor*product_uom.factor) as volume,
                    sum(l.price_subtotal / COALESCE(po.currency_rate, 1.0))::decimal(16,2) * currency_table.rate as untaxed_total,
                    sum(l.product_qty / line_uom.factor * product_uom.factor) as qty_ordered,
                    sum(l.qty_received / line_uom.factor * product_uom.factor) as qty_received,
                    sum(l.qty_invoiced / line_uom.factor * product_uom.factor) as qty_billed,
                    case when t.purchase_method = 'purchase' 
                         then sum(l.product_qty / line_uom.factor * product_uom.factor) - sum(l.qty_invoiced / line_uom.factor * product_uom.factor)
                         else sum(l.qty_received / line_uom.factor * product_uom.factor) - sum(l.qty_invoiced / line_uom.factor * product_uom.factor)
                    end as qty_to_be_billed,
            po.order_category as order_category,
            po.export_type as export_type,
            po.product_type as product_type
        """
        return select_str


