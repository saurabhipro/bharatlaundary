from odoo import models, fields, api

class BharatLaundaryService(models.Model):
    _name = 'bharatlaundary.service'
    _description = 'Bharat Laundary Service (Combo Choices)'
    _order = 'sequence, id'

    name = fields.Char(string='Service Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price')
    uom = fields.Char(string='Unit', help="e.g. Kg, Shirt")
    turnaround = fields.Char(string='Turnaround', help="e.g. 48 hrs Turnaround")
    packaging = fields.Char(string='Packaging', help="e.g. Combined Packaging")
    suitability = fields.Char(string='Suitable For', help="e.g. For Casual & Regular Wear")
    icon_class = fields.Char(string='Icon Class', default='fa-tint', help="FontAwesome class")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ecommerce_categ_id = fields.Many2one(
        'product.public.category', 
        string='eCommerce Category',
        compute='_compute_ecommerce_categ_id',
        store=True,
        help="Primary eCommerce category for grouping"
    )

    @api.depends('public_categ_ids')
    def _compute_ecommerce_categ_id(self):
        for record in self:
            if record.public_categ_ids:
                record.ecommerce_categ_id = record.public_categ_ids[0].id
            else:
                record.ecommerce_categ_id = False
