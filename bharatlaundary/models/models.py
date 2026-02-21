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
    service_tag_ids = fields.Many2many(related='product_id.product_tag_ids', string="Tags")

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    service_tag_ids = fields.Many2many(related='product_id.product_tag_ids', string="Tags")

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
    partner_mobile = fields.Char(compute='_compute_partner_mobile', string="Customer Contact", store=True)

    @api.depends('partner_id.mobile', 'partner_id.phone')
    def _compute_partner_mobile(self):
        for record in self:
            record.partner_mobile = record.partner_id.mobile or record.partner_id.phone or ''

    def action_print_laundry_tags(self):
        """ Button action to print laundry tags """
        return self.env.ref('bharatlaundary.action_report_laundry_tag').report_action(self)

    def _get_laundry_tags(self):
        """ Returns a list of tag data for the report with group counters """
        self.ensure_one()
        tags = []
        
        # Pass 1: Calculate Totals
        grand_total = 0
        group_totals = {} # {code: count}
        line_data = [] # List of dicts

        for line in self.order_line:
            # Determine Quantity
            qty = line.piece_count
            if qty <= 0:
                 qty = int(line.product_uom_qty) if line.product_uom_qty >= 1 else 1
            
            # Determine Service Code (Main Category)
            if line.service_tag_ids:
                code = line.service_tag_ids[0].name.upper()
            else:
                code = line.product_id.name[:2].upper() if line.product_id.name else "LD"
            
            grand_total += qty
            group_totals[code] = group_totals.get(code, 0) + qty
            
            line_data.append({
                'line': line,
                'qty': qty,
                'code': code
            })
        
        # Pass 2: Generate Tags
        group_counters = {} # {code: current_index}
        
        for item in line_data:
            line = item['line']
            qty = item['qty']
            code = item['code']
            product_name = line.product_id.name
            
            for _ in range(qty):
                # Increment counter for this specific code group
                group_counters[code] = group_counters.get(code, 0) + 1
                group_idx = group_counters[code]
                group_total = group_totals[code]
                
                tags.append({
                    'order_name': self.name,
                    'date': fields.Datetime.now().strftime('%m/%d/%y %H:%M'),
                    'customer_name': self.partner_id.name,
                    'product_name': product_name,       # Sub Category
                    'service_code': code,               # Main Category
                    'counter_str': f"{group_idx} / {group_total} / {grand_total}"
                })
        return tags

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    laundry_role = fields.Selection([
        ('admin', 'Shop Admin'),
        ('washer', 'Washer'),
        ('rider', 'Rider'),
        ('ironer', 'Ironer'),
    ], string="Laundry Role")
