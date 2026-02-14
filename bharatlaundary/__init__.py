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

        # Delete products that are not assigned to our legal categories
        # This is safer than 'not child_of' which is not a standard operator
        other_products = env['product.template'].search([('public_categ_ids', 'not in', legal_category_ids)])
        if other_products:
            other_products.unlink()
