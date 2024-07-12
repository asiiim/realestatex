from odoo import models, fields

class ComplaintStage(models.Model):
    _name = 'complaint.stage'
    _description = 'Complaint Stage'

    name = fields.Char(string='Stage Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
