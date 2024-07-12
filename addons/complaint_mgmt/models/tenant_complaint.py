from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied, ValidationError, UserError

class TenantComplaint(models.Model):
    _name = 'tenant.complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tenant Complaint'

    name = fields.Char(
        string='Complaint No.', 
        required=True,
        default='New',
        index='trigram',
        readonly=True
    )
    
    def get_possible_assignee(self):
        User = self.env['res.users']
        all_users = User.search([])
        Complaint = self.env['tenant.complaint']
        
        solved_stage = self.env.ref('complaint_mgmt.complaint_stage_solved').id
        dropped_stage = self.env.ref('complaint_mgmt.complaint_stage_dropped').id
        
        user_complaints = {user.id: Complaint.search_count([('assigned_to', '=', user.id)]) for user in all_users}
        
        feasible_users = [
            user for user in all_users
            if user_complaints[user.id] == 0 or
            Complaint.search_count([('assigned_to', '=', user.id), ('stage_id', 'in', [solved_stage, dropped_stage])]) > 0
        ]
        
        if feasible_users:
            return min(feasible_users, key=lambda u: user_complaints[u.id])
        
        return min(all_users, key=lambda u: user_complaints[u.id])
    
    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            # Get assignee for this complaint
            assignee = self.get_possible_assignee()
            values['assigned_to'] = assignee.id
            
            # Get a complaint no. during the submission of complaint from website form.
            if values.get('name', 'New') == 'New':
                values['name'] = self.env['ir.sequence'].next_by_code(
                    'ten.comp'
                ) or 'New'
                
            # Send email to customer representative.
            subject = _('New Complaint Assignment: %s') % (values['name'])
            body = '''
            Dear <b>%s</b><br/>,
            
            You have been assigned to new complaint <b>%s</b>.<br/>
            Please check and take needful action on it.<br/>
            Thank you.<br/>
            
            Regards,<br/>
            %s
            ''' % (
                assignee.name,
                values['name'],
                self.env.user.name
            )
            content = {
                'subject': subject,
                'author_id': self.env.user.partner_id.id,
                'body_html': body,
                'email_to': assignee.login,
            }
            self.env['mail.mail'].create(content).send()
        return super().create(vals_list)
    
    tenant_name = fields.Char(
        string='Tenant Name',
        tracking=2
    )
    email = fields.Char(
        string='Email', 
        required=True,
        tracking=2
    )
    address = fields.Char(
        string='Address', 
        required=True,
        tracking=3
    )
    type_id = fields.Many2one(
        'complaint.type', 
        string='Complaint Type', 
        required=True,
        tracking=3,
        default=lambda self: self._default_type()
    )
    question = fields.Boolean(related="type_id.question", store=True)
    description = fields.Text(
        string='Description', 
        required=True
    )
    stage_id = fields.Many2one(
        'complaint.stage', 
        string='Complaint Stage',
        tracking=3, 
        default=lambda self: self._default_stage()
    )
    action_plan = fields.Text(string='Action Plan', tracking=3)
    assigned_to = fields.Many2one('res.users', string='Assigned to')
    
    def reply_email(self):
        solved_stage = self.env.ref('complaint_mgmt.complaint_stage_solved')
        for rec in self:
            if rec.question and rec.action_plan:
                subject = _('Answer for your complaint question: %s') % (rec.name)
                body = '''
                Dear <b>%s</b>,<br/>
                
                %s<br/>
                
                Thank you.<br/>
                Regards,<br/>
                %s
                ''' % (
                    rec.tenant_name,
                    rec.action_plan,
                    rec.assigned_to.name
                )
                content = {
                    'subject': subject,
                    'author_id': rec.assigned_to.partner_id.id,
                    'body_html': body,
                    'email_to': rec.email,
                }
                self.env['mail.mail'].create(content).send()
                rec.stage_id = solved_stage
            else:
                raise UserError("Please fill up the response in action plan field before sending email response to tenant.")
            
    outcome = fields.Text("Complaint Outcome")

    @api.onchange('stage_id')
    def onchange_stage(self):
        solved_stage = self.env.ref('complaint_mgmt.complaint_stage_solved')
        dropped_stage = self.env.ref('complaint_mgmt.complaint_stage_dropped')
        
        if self.stage_id == solved_stage or self.stage_id == dropped_stage:
            if not self.outcome:
                raise UserError("Please fill up the outcome of this complaint before you set this as Solved or Dropped.")
            stage_state = ''
            if self.stage_id == solved_stage:
                stage_state = 'Solved'
            elif self.stage_id == dropped_stage:
                stage_state = 'Dropped'
            
            subject = _('You Complaint %s has been %s') % (self.name, stage_state)
            body = '''
            Dear <b>%s</b>,<br/>
            Your complaint (ref: %s) has been <b>%s</b>.<br/>
            %s<br/>
            Thank you.<br/>
            Regards,<br/>
            %s
            ''' % (
                self.tenant_name,
                self.name,
                stage_state,
                self.outcome,
                self.assigned_to.name
            )
            content = {
                'subject': subject,
                'author_id': self.assigned_to.partner_id.id,
                'body_html': body,
                'email_to': self.email,
            }
            print("\n\n\nContent:", content)
            self.env['mail.mail'].create(content).send()
            
    @api.onchange('action_plan')
    def onchange_action_plan(self):
        if self.action_plan:
            self.stage_id = self.env.ref('complaint_mgmt.complaint_stage_in_progress')
        else:
            self.stage_id = self.env.ref('complaint_mgmt.complaint_stage_in_review')
            
    @api.model
    def _default_type(self):
        return self.env['complaint.type'].search([], limit=1).id
   
    @api.model
    def _default_stage(self):
        return self.env['complaint.stage'].search([], limit=1).id