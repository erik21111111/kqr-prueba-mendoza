{
    'name': 'Pallet SSCC',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Assign a unique GS1 SSCC to each pallet (stock.package)',
    'author': 'Erik Mendoza',
    'depends': ['stock'],
    'data': [
        'views/res_company_views.xml',
        'views/stock_package_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
