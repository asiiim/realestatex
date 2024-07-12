{
    'name': "Tenant Complaint Mgmt",
    'version': '17.0.0.1',
    'category': 'Base',
    'sequence': -1,
    'author': 'Aashim Bajracharya',
    'summary': "Manage tenant complaints",
    'description': '''
        1. ...
    ''',
    'depends': ['base', 'website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/complaint.xml',
        'views/complaint_portal.xml',
        'data/ir_sequence.xml',
        'data/complaint_stages.xml',
        'data/complaint_types.xml',
        'data/website_data.xml',
        'reports/paper_formats.xml',
        'reports/work_order.xml',
    ],
    'application': True,
}
