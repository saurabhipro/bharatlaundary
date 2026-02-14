from . import models
from . import controllers

def post_init_hook(env):
    """
    Clean up default Odoo products and categories to ensure only 
    Bharat Laundry data is present.
    """
    # Find our root category
    root_category = env.ref('bharatlaundary.product_category_bharatlaundary', raise_if_not_found=False)
    
    # 1. Clean up website pages (Delete default Pricing page)
    pages = env['website.page'].search([('url', '=', '/pricing')])
    if pages:
        pages.unlink()

    if root_category:
        # Get all legal categories (root and its children)
        legal_category_ids = env['product.public.category'].search([('id', 'child_of', root_category.id)]).ids
        # Find and delete all other categories
        other_categories = env['product.public.category'].search([('id', 'not in', legal_category_ids)])
        if other_categories:
            other_categories.unlink()

        # Update all products in our Categories to be 'service' type
        # This fixes products that were imported as 'consu' or 'product' previously
        our_products = env['product.template'].search([('public_categ_ids', 'in', legal_category_ids)])
        if our_products:
            our_products.write({
                'type': 'service',
                'website_published': True,
            })
            # Force recompute of our new grouping field
            our_products._compute_ecommerce_categ_id()

        # Delete products that are not assigned to our legal categories
        other_products = env['product.template'].search([('public_categ_ids', 'not in', legal_category_ids)])
        if other_products:
            other_products.unlink()

    # 2. Configure COD (Cash on Delivery)
    cod_provider = env['payment.provider'].search([('code', '=', 'transfer')], limit=1)
    if cod_provider:
        cod_provider.write({
            'name': 'Cash on Delivery (COD)',
            'display_as': 'Cash on Delivery',
            'state': 'enabled',
            'is_published': True,
            'pending_msg': '<p>Your order has been confirmed. Please keep the cash ready at the time of delivery.</p>',
        })
        cod_provider.website_id = False
        
        # Link payment methods (Needed in Odoo 17/18)
        transfer_method = env['payment.method'].search([('code', '=', 'transfer')], limit=1)
        if transfer_method and transfer_method not in cod_provider.payment_method_ids:
            cod_provider.payment_method_ids = [(4, transfer_method.id)]
