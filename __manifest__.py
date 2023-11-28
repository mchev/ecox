{
	'name': 'Ecorobotix Traceability',
	'version': '1.0',
	'author': 'Martin Chevignard',
	'website': 'https://martinchevignard.com',
	'summary': 'Custom report views',
    'license': 'OEEL-1',
    'category': 'Inventory/Inventory',
    'depends': ['product', 'mrp'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/recursive_serial_search_view.xml',
        'views/ecox_test_view.xml',
    ]
}