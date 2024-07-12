from odoo import models, fields

class ComplaintType(models.Model):
    _name = 'complaint.type'
    _description = 'Complaint Type'

    name = fields.Char(string='Type', required=True)
    question = fields.Boolean("Is Question?", default=False)