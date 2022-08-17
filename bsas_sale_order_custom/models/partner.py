from odoo import models, fields, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Notify'),
         ('delivery', 'Consignee'),
         ('other', 'Other Address'),
         ("private", "Private Address"),
         ], string='Address Type',
        default='contact',
        help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")

    # customer_type_id = fields.Many2one(comodel_name="res.partner.type", string="Customer Type")
    insurance_type = fields.Selection(string="", selection=[('yes', 'Yes'), ('no', 'No'), ],)
    insurance_credit_limit = fields.Float(string="Insurance Credit Limit")
    insurance_currency_id = fields.Many2one(comodel_name="res.currency")
    # insurance_company = fields.Char(string="Insurance Company")
    continent = fields.Selection(string="Continent", selection=[('Africa', 'Africa'), ('Antarctica', 'Antarctica'),
                                                   ('Asia', 'Asia'),('Australia', 'Australia'),('Europe', 'Europe'),
                                                   ('North_America', 'North America'),('South_America', 'South America')
                                                   ],default='Africa')


    @api.onchange('insurance_type')
    def _set_insurance_credit_limit(self):
        self.insurance_credit_limit=0.0
        self.insurance_currency_id=False
        # self.insurance_company=""

    # def _get_name(self):
    #     res=super(ResPartnerInherit, self)._get_name()
    #     if self.continent:
    #         res = "%s \n %s" % (res, self.continent)
    #     return res