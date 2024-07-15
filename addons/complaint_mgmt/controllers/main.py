from odoo import http
from odoo.http import request

class TenantComplaintController(http.Controller):

    @http.route('/complaint/form', type='http', auth='public', website=True)
    def complaint_form(self, **kwargs):
        complaint_types = request.env['complaint.type'].sudo().search([])
        return request.render('complaint_mgmt.complaint_form', {
            'complaint_types': complaint_types,
        })

    @http.route('/complaint/submit', type='http', auth='public', methods=['POST'], website=True)
    def complaint_submit(self, **post):
        complaint = request.env['tenant.complaint'].sudo().create({
            'tenant_name': post.get('tenant_name'),
            'email': post.get('email'),
            'address': post.get('address'),
            'type_id': int(post.get('type_id')),
            'description': post.get('description'),
            'assigned_to': request.env.user.id,
        })
        return request.render('complaint_mgmt.complaint_submission_success', {
            'complaint': complaint,
        })
