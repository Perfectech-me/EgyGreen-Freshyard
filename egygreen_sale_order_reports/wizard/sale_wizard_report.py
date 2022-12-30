from odoo import models, fields, api
class SaleWizardReport(models.TransientModel):
    _name = 'sale.wizard.report'


    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    partner_ids = fields.Many2many(comodel_name="res.partner",  relation="par_id", column1="partner", column2="colum_part2",string="Customer")
    continent = fields.Selection(string="Continent", selection=[('Africa', 'Africa'), ('Antarctica', 'Antarctica'),
                                                                ('Asia', 'Asia'), ('Australia', 'Australia'),
                                                                ('Europe', 'Europe'),
                                                                ('North_America', 'North America'),
                                                                ('South_America', 'South America')
                                                                ], default='Africa')
    country_ids = fields.Many2many(comodel_name="res.country", string="Country")
    order_category = fields.Selection(string="Order Catrgory", selection=[
        ('International', 'International'),
        ('Local', 'Local'),
    ], default='International')

    export_type = fields.Selection(string="Order Type", selection=[('fresh', 'fresh'), ('frozen', 'frozen'),
                                                                    ('food_products', 'Food Products'),
                                                                    ('service', 'Service'),
                                                                    ('other', 'Other'),
                                                             ])

    packing_place_id = fields.Many2one(comodel_name="res.partner", string="Packing Place")
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytical  Account")
    discharge_country_id = fields.Many2one(comodel_name="res.country", string="Place Of Discharge")

    incoterm_id = fields.Many2one(comodel_name="account.incoterms", string="Incoterm")
    pricelist_id = fields.Many2one(comodel_name="product.pricelist", string="Pricelist")
    #
    partner_shipping_ids = fields.Many2many(comodel_name="res.partner", relation="shigpping_id", column1="parts_shipping", column2="colums_shipping", string="Freight Forwarder", )
    partner_clearance_ids = fields.Many2many(comodel_name="res.partner", relation="clearances_id", column1="parts_clearance", column2="colums_clearance", string="Clearance Company", )
    partner_insurance_ids = fields.Many2many(comodel_name="res.partner", relation="insurances_id", column1="parts_insurance", column2="colums_insurance", string="Insurance Company", )
    shipping_type = fields.Selection(string="Shipping Type", selection=[('Air', 'Air'), ('Ocean', 'Ocean'),('Land', 'Land')])
    #
    sales_person_user_ids = fields.Many2many(comodel_name="res.users",string="Sales Person")


    def button_print(self):
        return self.env.ref('egygreen_sale_order_reports.sale_wizard_report_xlsx').report_action(self)
