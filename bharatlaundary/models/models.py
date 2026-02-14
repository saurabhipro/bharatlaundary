from odoo import models, fields, api

class BharatLaundaryService(models.Model):
    _name = 'bharatlaundary.service'
    _description = 'Bharat Laundary Service'

    name = fields.Char(string='Service Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
