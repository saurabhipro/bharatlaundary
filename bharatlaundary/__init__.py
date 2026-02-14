from . import models

def post_init_hook(env):
    """
    Clean up default Odoo products and categories to ensure only 
    Bharat Laundry data is present.
    """
    # Find our root category
    root_category = env.ref('bharatlaundary.product_category_bharatlaundary', raise_if_not_found=False)
    
    
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
