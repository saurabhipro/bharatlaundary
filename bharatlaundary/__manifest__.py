{
    'name': "Bharat Laundary Core",
    'version': '1.1',
    'summary': "Core module for Bharat Laundary operations",
    'description': """
Bharat Laundary Core Module
===========================
Handles backend logic for Bharat Laundary.
    """,
    'author': "Bharat Laundary Team",
    'website': "http://www.bharatlaundary.com",
    'category': 'Services',
    'depends': ['base', 'product', 'website', 'website_sale', 'payment_custom', 'hr', 'sale', 'account', 'barcodes', 'crm', 'sale_crm'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/employee_views.xml',
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
        'report/laundry_tag_report.xml',
        'data/data.xml',
        'data/products.xml',
        'data/combos.xml',
        'data/order.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bharatlaundary/static/src/css/style.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'post_init_hook': 'post_init_hook',
    'license': 'LGPL-3',
}
