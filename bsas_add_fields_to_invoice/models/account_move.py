from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    original_bl=fields.Boolean(string='Original BL', default=False)
    telex_release = fields.Boolean(string='Telex release', default=False)
    prepaid = fields.Boolean(string='prepaid', default=False)
    collect = fields.Boolean(string='Collect', default=False)
    subsidies_latter_yes = fields.Boolean(string='Yes', default=False)
    subsidies_latter_no = fields.Boolean(string='No', default=False)


    @api.onchange('subsidies_latter_yes')
    def subsidies_latteryes(self):
        for rec in self:
            if rec.subsidies_latter_yes==True:
             rec.subsidies_latter_no= False
            else:
                rec.subsidies_latter_no=True

    @api.onchange('subsidies_latter_no')
    def subsidies_latterno(self):
        for rec in self:
            if rec.subsidies_latter_no==True:
                rec.subsidies_latter_yes = False
            else:
                rec.subsidies_latter_yes = True

