from odoo import models, fields, api, _


class Project(models.Model):
    _name = 'project.management.project'
    _description = 'Project'
    _inherit = ['mail.thread']

    name = fields.Char(string="Project Name", required=True, tracking=True)
    code = fields.Char(
        string="Code",
        default=lambda self: self.env['ir.sequence'].next_by_code('project.management.project'),
        copy=False,
        readonly=True,
    )
    description = fields.Text(string="Description")

    task_ids = fields.One2many(
        'project.management.task',
        'project_id',
        string="Tasks",
    )

    progress = fields.Float(
        string="Progress %",
        compute='_compute_progress',
        store=True,
    )

    manager_id = fields.Many2one(
        'hr.employee',
        string="Project Manager",
    )

    @api.depends('task_ids.stage_id.is_final')
    def _compute_progress(self):
        for proj in self:
            total = len(proj.task_ids)
            done  = len([
                t for t in proj.task_ids
                if t.stage_id and t.stage_id.is_final
            ])
            proj.progress = done * 100.0 / total if total else 0.0
