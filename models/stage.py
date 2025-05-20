from odoo import models, fields

class ProjectStage(models.Model):
    _name = 'project.management.stage'
    _description = 'Task Stage'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean(string="Folded in Kanban")
    is_final = fields.Boolean(string="Final Stage")