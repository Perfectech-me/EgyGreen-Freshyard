# -*- coding: utf-8 -*-
from odoo import models, api, exceptions



class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'


    @api.model
    def create(self, vals):
        if not self.env.user.has_group('accounting_access_groups.group_partner_create'):
            raise exceptions.ValidationError("You do not have the permission to create partner.")
        return super(ResPartnerInherit, self).create(vals)

    def write(self, vals):
        if not self.env.user.has_group('accounting_access_groups.group_partner_edit'):
            raise exceptions.ValidationError("You do not have the permission to edit partner.")
        return super(ResPartnerInherit, self).write(vals)


