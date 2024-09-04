# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2020-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError

import babel
import time
from datetime import datetime, timedelta
import pytz


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'
    att_policy_id = fields.Many2one('hr.attendance.policy',
                                    string='Attendance Policy')


    shifts_line_id = fields.Many2one('resource.calendar',string="Shifts")



class HRemp(models.Model):
    _inherit="hr.employee"

    def get_employee_shifts(self, day_start, day_end, tz):
        self.ensure_one()
        plan_slot_obj = self.env['planning.slot']
        day_start_native = day_start.replace(tzinfo=tz).astimezone(
            pytz.utc).replace(tzinfo=None)
        day_end_native = day_end.replace(tzinfo=tz).astimezone(
            pytz.utc).replace(tzinfo=None)
        slot_ids = plan_slot_obj.search(
            [('employee_id','=',self.id),
             ('start_datetime', '>=', day_start_native),
             ('start_datetime', '<=', day_end_native)])
        working_intervals = []
        for slot in slot_ids:
            working_intervals.append((slot.start_datetime, slot.end_datetime))
        return working_intervals

#
# class ResourceCalendar(models.Model):
#     _inherit = 'resource.calendar'
#     shifts_record_id = fields.Many2one("hr.contract")
#
