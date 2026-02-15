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

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    piece_count = fields.Integer(string="Pieces", default=1, help="Number of physical items/tags to generate")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    laundry_state = fields.Selection([
        ('draft', 'Quotation'),
        ('picked', 'Picked Up'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
    ], string="Laundry Status", default='draft', tracking=True)

    rider_id = fields.Many2one('hr.employee', string="Pickup/Delivery Rider", domain=[('laundry_role', '=', 'rider')])

    def _get_laundry_tags(self):
        """ Returns a list of tag data for the report """
        self.ensure_one()
        tags = []
        # Calculate total count of items based on piece_count with fallback logic
        total_count = 0
        for line in self.order_line:
            p_qty = line.piece_count
            if p_qty <= 0:
                 p_qty = int(line.product_uom_qty) if line.product_uom_qty >= 1 else 1
            total_count += p_qty
        
        current_idx = 1
        for line in self.order_line:
            # Use piece_count for number of tags
            qty = line.piece_count
            if qty <= 0:
                # Fallback to uom_qty if piece_count is 0 or negative (though default is 1)
                qty = int(line.product_uom_qty) if line.product_uom_qty >= 1 else 1
            
            # Service abbreviation (first 2 letters)
            service_code = line.product_id.name[:2].upper() if line.product_id.name else "LD"
            
            for _ in range(qty):
                tags.append({
                    'index': current_idx,
                    'total': total_count,
                    'product_name': line.product_id.name,
                    'service_code': service_code,
                    'customer_name': self.partner_id.name,
                    'order_name': self.name,
                    'date': fields.Datetime.now().strftime('%m/%d/%y, %I:%M %p'),
                })
                current_idx += 1
        return tags

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    laundry_role = fields.Selection([
        ('admin', 'Shop Admin'),
        ('washer', 'Washer'),
        ('rider', 'Rider'),
        ('ironer', 'Ironer'),
    ], string="Laundry Role")
