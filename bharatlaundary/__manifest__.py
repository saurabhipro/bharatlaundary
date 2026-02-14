{
    'name': "Bharat Laundary Core",
    'version': '1.0',
    'summary': "Core module for Bharat Laundary operations",
    'description': """
Bharat Laundary Core Module
===========================
Handles backend logic for Bharat Laundary.
    """,
    'author': "Bharat Laundary Team",
    'website': "http://www.bharatlaundary.com",
    'category': 'Services',
    'depends': ['base', 'product', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
        'data/products.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'post_init_hook': 'post_init_hook',
    'license': 'LGPL-3',
}
