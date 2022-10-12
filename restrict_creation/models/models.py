# -*- coding: utf-8 -*-
from num2words import num2words

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta



class BarcodeNomenclature(models.Model):
    _inherit = 'barcode.nomenclature'

    @api.model
    def create(self, vals):
        # create view location for warehouse then create all locations
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        # actually create WH
        warehouse = super(BarcodeNomenclature, self).create(vals)

        return warehouse

    def write(self, vals):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(BarcodeNomenclature, self).write(vals)

        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(BarcodeNomenclature, self).unlink()

        return res

class UomCategory(models.Model):
    _inherit = 'uom.category'

    @api.model
    def create(self, vals):
        # create view location for warehouse then create all locations
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        # actually create WH
        warehouse = super(UomCategory, self).create(vals)

        return warehouse

    def write(self, vals):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(UomCategory, self).write(vals)

        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(UomCategory, self).unlink()

        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))

        templates = super(ProductTemplate, self).create(vals_list)
        # `_get_variant_id_for_combination` depends on existing variants
        return templates

    def write(self, vals):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))

        self._sanitize_vals(vals)

        if 'uom_id' in vals or 'uom_po_id' in vals:
            uom_id = self.env['uom.uom'].browse(vals.get('uom_id')) or self.uom_id
            uom_po_id = self.env['uom.uom'].browse(vals.get('uom_po_id')) or self.uom_po_id
            if uom_id and uom_po_id and uom_id.category_id != uom_po_id.category_id:
                vals['uom_po_id'] = uom_id.id
        res = super(ProductTemplate, self).write(vals)
        return res

class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.model_create_multi
    def create(self,vals_list):
        print("accountaccount")
        templates = super(AccountAccount, self).create(vals_list)
        return templates

class Warehouse(models.Model):
    _inherit = "stock.warehouse"
    @api.model
    def create(self, vals):
        # create view location for warehouse then create all locations
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        # actually create WH
        warehouse = super(Warehouse, self).create(vals)

        return warehouse
    def write(self, vals):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Warehouse, self).write(vals)

        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Warehouse, self).unlink()

        return res

class Location(models.Model):
    _inherit = "stock.location"
    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Location, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Location, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Location, self).unlink()
        return res


class Rule(models.Model):
    _inherit = "stock.rule"
    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Rule, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Rule, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Rule, self).unlink()
        return res


class Route(models.Model):
    _inherit = "stock.location.route"
    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Route, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Route, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(Route, self).unlink()
        return res


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"
    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockPickingType, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockPickingType, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockPickingType, self).unlink()
        return res

class StockPutawayRule(models.Model):
    _inherit = "stock.putaway.rule"
    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockPutawayRule, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockPutawayRule, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockPutawayRule, self).unlink()
        return res


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"
    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(DeliveryCarrier, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(DeliveryCarrier, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(DeliveryCarrier, self).unlink()
        return res




class ProductAttribute(models.Model):
    _inherit = "product.attribute"


    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(ProductAttribute, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(ProductAttribute, self).write(values)
        return res
    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(ProductAttribute, self).unlink()
        return res

class ProductCategory(models.Model):
    _inherit = "product.category"

    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(ProductCategory, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(ProductCategory, self).write(values)
        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(ProductCategory, self).unlink()
        return res




class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockQuant, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockQuant, self).write(values)
        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockQuant, self).unlink()
        return res

class StockScrap(models.Model):
    _inherit = "stock.scrap"

    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockScrap, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockScrap, self).write(values)
        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockScrap, self).unlink()
        return res

class StockStorageCategoryCapacity(models.Model):
    _inherit = "stock.storage.category.capacity"

    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockStorageCategoryCapacity, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockStorageCategoryCapacity, self).write(values)
        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockStorageCategoryCapacity, self).unlink()
        return res


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model_create_multi
    def create(self, vals_list):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockWarehouseOrderpoint, self).create(vals_list)
        return res

    def write(self, values):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockWarehouseOrderpoint, self).write(values)
        return res

    def unlink(self):
        if self.user_has_groups('restrict_creation.group_restrict_creation'):
            raise UserError(_('You cannot do this operation please contact admin'))
        res = super(StockWarehouseOrderpoint, self).unlink()
        return res



