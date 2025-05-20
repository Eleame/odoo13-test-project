# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class TaskFilterWizard(models.TransientModel):
    """
    A pop-up wizard for filtering tasks.
    The "Apply Filter" button remains in the same window and
    shows a table of found tasks.
    """
    _name = 'project.management.task.filter.wizard'
    _description = 'Task Filter Wizard'

    # ───── Filters ──────────────────────────────────────────────
    project_id  = fields.Many2one(
        'project.management.project',
        string="Project",
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
    )
    date_from   = fields.Date(string="From")
    date_to     = fields.Date(string="To")

    # ───── Founded Tasks ────────────────────────────────────
    task_ids = fields.Many2many(
        'project.management.task',
        string="Tasks",
        compute='_compute_task_ids',
        readonly=True,
    )

    @api.depends('project_id', 'employee_id', 'date_from', 'date_to')
    def _compute_task_ids(self):
        Task = self.env['project.management.task'].sudo()
        for wiz in self:
            domain = []
            if wiz.project_id:
                domain.append(('project_id', '=', wiz.project_id.id))
            if wiz.employee_id:
                # hr.employee → res.users → task.user_ids
                domain.append(('user_ids.employee_ids', 'in', wiz.employee_id.id))
            if wiz.date_from:
                domain.append(('create_date', '>=', wiz.date_from))
            if wiz.date_to:
                domain.append(('create_date', '<=', wiz.date_to))
            wiz.task_ids = Task.search(domain)

    def action_filter(self):
        """
        We return a full-fledged act_window so that the web client
        doesn't complain about "No type for action".
        """
        self.ensure_one()
        self._compute_task_ids()

        view = self.env.ref('project_management.view_task_filter_wizard_form')

        return {
            'type'     : 'ir.actions.act_window',
            'name'     : _('Filter Tasks'),
            'res_model': 'project.management.task.filter.wizard',
            'view_mode': 'form',
            'res_id'   : self.id,
            'target'   : 'new',
            'views'    : [(view.id, 'form')],
            'view_id'  : view.id,
        }
