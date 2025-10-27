from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    internal_code = fields.Char(
        string='Codigo Interno',
        help='Internal reference code for the contact',
        copy=False,
        index=True
    )
    
    _sql_constraints = [
        ('internal_code_uniq', 'unique(internal_code)', 'Internal Code must be unique!'),
    ]