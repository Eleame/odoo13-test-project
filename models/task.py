# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import api, fields, models, _


class Task(models.Model):
    _name = 'project.management.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Task Name", required=True, tracking=True)
    description = fields.Text(string="Description")

    project_id = fields.Many2one(
        'project.management.project',
        string="Project",
        required=True,
        tracking=True,
    )

    def _default_stage(self):
        return self.env['project.management.stage'].search([], limit=1)

    stage_id = fields.Many2one(
        'project.management.stage',
        string="Stage",
        default=_default_stage,
        tracking=True,
    )

    stage_is_final = fields.Boolean(
        string="Stage is final",
        related='stage_id.is_final',
        store=True,
    )

    user_ids = fields.Many2many(
        'hr.employee',
        string="Assigned Employees",
        tracking=True,
    )

    priority = fields.Selection(
        [('0', 'Normal'), ('1', 'High')],
        default='0',
    )

    planned_start = fields.Date(string="Planned Start")
    planned_end   = fields.Date(string="Planned End")

    is_overdue = fields.Boolean(
        string="Overdue",
        compute='_compute_overdue',
        store=True,
    )

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec.message_post(body=_("Task created"))
        rec._send_stage_change_email(is_new=True)
        return rec

    def write(self, vals):
        stage_changed = 'stage_id' in vals
        old_stage = {t.id: t.stage_id for t in self} if stage_changed else {}
        res = super().write(vals)

        if stage_changed:
            for task in self:
                if old_stage[task.id] != task.stage_id:
                    task.message_post(body=_("Task stage changed to: %s") %
                                      task.stage_id.name)
                    if task.stage_is_final:
                        task.message_post(body=_("Task completed"))
                    task._send_stage_change_email()
        return res

    def _send_stage_change_email(self, is_new=False):
        template = self.env.ref(
            'project_management.mail_template_task_stage_changed',
            raise_if_not_found=False,
        )
        if not template:
            return
        for task in self:
            if task.user_ids:
                template.with_context(is_new=is_new).send_mail(
                    task.id, force_send=True,
                )

    @api.depends('planned_end', 'stage_is_final')
    def _compute_overdue(self):
        today = date.today()
        for t in self:
            t.is_overdue = bool(
                t.planned_end and t.planned_end < today and not t.stage_is_final
            )

    @classmethod
    def _cron_notify_overdue(cls):
        today = date.today()
        tasks = cls.search([
            ('planned_end', '<', today),
            ('stage_is_final', '=', False),
        ])
        for task in tasks:
            task.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=today + timedelta(days=1),
                note=_('Task is overdue'),
            )

    def _track_subtype(self, init_values):
        if 'stage_id' in init_values:
            return self.env.ref('mail.mt_note')
        return super()._track_subtype(init_values)
