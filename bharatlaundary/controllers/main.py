from odoo import http
from odoo.http import request

class BharatLaundaryWebsite(http.Controller):

    @http.route(['/bharatlaundary', '/bharatlaundary/home'], type='http', auth="public", website=True)
    def index(self, **kwargs):
        combos = request.env['bharatlaundary.service'].search([('active', '=', True)])
        return request.render("bharatlaundary.homepage", {
            'combos': combos,
        })

    @http.route(['/rate-list', '/pricing'], type='http', auth="public", website=True)
    def rate_list(self, **kwargs):
        # Search for categories that are children of the Bharat Laundary root category
        root_category = request.env.ref('bharatlaundary.product_category_bharatlaundary', raise_if_not_found=False)
        categories = request.env['product.public.category']
        if root_category:
            categories = request.env['product.public.category'].search([('id', 'child_of', root_category.id), ('id', '!=', root_category.id)])
        
        return request.render("bharatlaundary.rate_list_page", {
            'categories': categories,
        })
