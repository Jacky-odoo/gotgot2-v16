{
    'name': 'Opt Patient',
    'description': 'Hospital Patient',
    'author': '',
    'application': False,
    'depends':['opt_custom'],
    'data': [
        'security/ir.model.access.csv', 
        'opt_patient_view.xml',
        # 'security/security.xml',
        # 'security/opt_patient_access_rules.xml',
    ],
}
