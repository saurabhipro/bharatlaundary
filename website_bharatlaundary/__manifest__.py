{
    'name': "Bharat Laundary Website",
    'version': '1.0',
    'summary': "Simple, Clean website for Bharat Laundary",
    'description': """
Bharat Laundary: Simple Website Module
======================================
Provides a clean, professional landing page and services overview for Bharat Laundary.
Key Features:
- Hero Banner
- Services Grid
- Contact Information
- Direct link to Shop
    """,
    'author': "Bharat Laundary Team",
    'website': "http://www.bharatlaundary.com",
    'category': 'Website',
    'depends': ['website', 'website_sale', 'bharatlaundary'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_bharatlaundary/static/src/css/style.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
