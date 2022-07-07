
import odoo.osv.osv
from odoo import osv
from odoo import models, api
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)
class crm_routing_users(osv.osv):
    """For each Department and Role, which user is the responsible"""
    _name = "crm.routing.users"

    def _migrate_from_project_issue_profiling(self, cr, uid, ids=None, context=None):
        """Migrate from project.issue.profiling. since this module can completely replace it."""
        if ids is not None:
            raise NotImplementedError("Ids is just there by convention! Please don't use it.")
        cr.execute("select exists(select * from information_schema.tables " "where table_name=project_issue_profiling)")
        if cr.fetchone()[0]:
            cr.execute(""" INSERT INTO crm_routing_users ( create_uid, create_date, write_date, write_uid, notes, user_id, section_id, department_id) SELECT create_uid, create_date, write_date, write_uid, notes, user_id, section_id, department_id FROM project_issue_profiling""")
            _logger.info("Successful data copy from project.issue.profiling to crm.routing.users")
            return True