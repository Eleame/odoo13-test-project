from odoo.tests.common import SavepointCase, tagged
from datetime import date, timedelta

@tagged('pm')
class TestProjectManagement(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Project = cls.env['project.management.project']
        cls.Task = cls.env['project.management.task']
        cls.HrEmployee = cls.env['hr.employee']

        cls.emp_demo = cls.HrEmployee.create({'name': 'Demo Emp'})
        cls.emp_other = cls.HrEmployee.create({'name': 'Other Emp'})

        cls.project = cls.Project.create({'name': 'Proj A'})
        cls.task1 = cls.Task.create({
            'name': 'Task 1',
            'project_id': cls.project.id,
            'user_ids': [(6, 0, cls.emp_demo.ids)],
        })
        cls.task2 = cls.Task.create({
            'name': 'Task 2',
            'project_id': cls.project.id,
            'user_ids': [(6, 0, cls.emp_other.ids)],
        })

    # --- CRUD --------------------------------------------------------------
    def test_01_state_change_posts_message(self):
        self.task1.stage_id = self.env['project.management.stage'].create({'name': 'Doing'})
        last_msg = self.task1.message_ids[:1].body
        self.assertIn('Stage', last_msg)

    # --- Wizard -----------------------------------------------------------
    def test_02_wizard_filters_by_employee(self):
        wiz = self.env['project.management.task.filter.wizard'].create({
            'employee_id': self.emp_demo.id,
        })
        action = wiz.action_filter()
        dom = self.env['ir.actions.actions']._get_eval_context(action)['domain']
        tasks = self.Task.search(dom)
        self.assertEqual(tasks, self.task1)

    # --- Security ---------------------------------------
    def test_03_security_user_can_only_see_his_tasks(self):
        user_demo = self.env['res.users'].create({
            'name': 'User Demo', 'login': 'udemo',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
            'employee_ids': [(6, 0, self.emp_demo.ids)],
        })
        task_visible = self.Task.with_user(user_demo).search([])
        self.assertEqual(task_visible, self.task1)

    # --- PDF ---------------------------------------------------------
    def test_04_qweb_report_renders(self):
        report = self.env.ref('project_management.action_report_tasks')
        pdf = report._render_qweb_pdf(self.task1.ids)[0]
        self.assertGreater(len(pdf), 1000) 

    # --- Kanban ------------------------------
    def test_05_drag_drop_updates_state(self):
        self.task1.with_context(kanban_state_change=True).write({'stage_id': self.env['project.management.stage'].create({'name': 'Done', 'is_final': True}).id})
        self.assertTrue(self.task1.stage_id.is_final)

