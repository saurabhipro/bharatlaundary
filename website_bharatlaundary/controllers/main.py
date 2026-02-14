from odoo import http
from odoo.http import request

class BharatLaundaryWebsite(http.Controller):

    @http.route(['/bharatlaundary', '/bharatlaundary/home'], type='http', auth="public", website=True)
    def index(self, **kwargs):
        return request.render("website_bharatlaundary.homepage", {})

    @http.route(['/rate-list'], type='http', auth="public", website=True)
    def rate_list(self, **kwargs):
        categories = request.env['product.public.category'].search([('parent_id.name', '=', 'Bharat Laundary')])
        return request.render("website_bharatlaundary.rate_list_page", {
            'categories': categories,
        })
