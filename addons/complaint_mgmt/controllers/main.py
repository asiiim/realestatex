from odoo import http
from odoo.http import request

class ComplaintController(http.Controller):

    @http.route(['/complaint/submit'], type='http', auth='public', website=True)
    def complaint_form(self, **kwargs):
        complaint_types = request.env['complaint.type'].search([])
        return request.render('complaint_mgmt.complaint_form', {
            'complaint_types': complaint_types
        })

    @http.route(['/complaint/submit'], type='http', methods=['POST'], auth='public', website=True)
    def submit_complaint(self, **post):
        complaint = request.env['tenant.complaint'].create({
            'tenant_name': post.get('tenant_name'),
            'email': post.get('email'),
            'address': post.get('address'),
            'type_id': int(post.get('type_id')),
            'description': post.get('description'),
        })
        return request.render('complaint_mgmt.complaint_thank_you', {'complaint': complaint})
