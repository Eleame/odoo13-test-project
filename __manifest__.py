{
    'name': "Project Management",
    'version': '13.0.3.0.0',
    'author': "Oleg",
    'category': 'Project',
    'summary': 'Advanced project & task management with progress tracking, SLA and reports.',
    'application': True,
    'depends': [
        'base',
        'mail',
        'hr',
        'web',
        'hr_org_chart',
    ],
    'data': [
        'security/project_groups.xml',
        'security/ir.model.access.csv',
        'security/stage_access.xml',
        'security/project_management_security.xml',
        'security/project_management_admin_acl.xml',

        'data/project_sequence.xml',
        'data/project_default_stages.xml',
        'data/cron.xml',
        'data/mail_templates.xml',

        'views/assets.xml',
        'views/actions.xml',
        'views/wizard_views.xml',
        'views/project_views.xml',
        'views/stage_views.xml',
        'views/task_views.xml',
        'views/menus.xml',
        'views/dashboard_views.xml',
        
        'report/task_report_templates.xml',
        'report/task_report.xml',
    ],
    'demo': [],
    'test': ['tests/test_project_management.py'],
    'installable': True,
}
