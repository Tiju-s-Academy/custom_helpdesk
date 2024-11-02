{
    'name': 'Helpdesk',
    'version': '17.0.1.0.0',
    'summary': 'Help Desk Management System',
    'depends': ['base', 'mail', 'web', 'project'],
    'data': [
        'data/mail_activity_data.xml',
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_team_views.xml',
        'views/helpdesk_category_views.xml',
        'views/helpdesk_category_dash.xml',
        'views/web_form.xml',
        'views/helpdesk_menu_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
