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

    @http.route(['/services'], type='http', auth="public", website=True)
    def services_page(self, **kwargs):
        return request.render("bharatlaundary.services_page")

    @http.route(['/bharatlaundary/schedule/submit'], type='http', auth="public", website=True, methods=['POST'], csrf=False)
    def schedule_submit(self, **post):
        contact_name = post.get('name')
        mobile = post.get('mobile')
        address = post.get('address')
        pickup_time = post.get('pickup_datetime')

        if not contact_name or not mobile:
             return request.render("bharatlaundary.homepage", {
                'form_error': "Name and Mobile are required.",
                'combos': request.env['bharatlaundary.service'].search([('active', '=', True)])
            })

        description = f"Address: {address}\nPickup Time: {pickup_time}"
        
        # Create Lead
        request.env['crm.lead'].sudo().create({
            'name': f"Pickup Request from {contact_name}",
            'contact_name': contact_name,
            'mobile': mobile,
            'description': description,
            'type': 'opportunity',
        })
        
        # Redirect to thank you page or show success message on homepage
        return request.render("bharatlaundary.thank_you_page", {
            'name': contact_name,
        })

    @http.route(['/thank-you'], type='http', auth="public", website=True)
    def thank_you_page(self, **kwargs):
         return request.render("bharatlaundary.thank_you_page")
