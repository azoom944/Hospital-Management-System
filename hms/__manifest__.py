{
    'name': "HMS",
    'description': "HMS Project",
    'author': "Azoom Samir",
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': ['base',
                'crm'],
    'application': True,
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/base.xml',
        'views/patient.xml',
        'views/department.xml',
        'views/doctor.xml',
        'views/crm_inherit.xml',
        'reports/patient_print.xml',
        'wizard/add_log_wizard.xml'
    ],
}
