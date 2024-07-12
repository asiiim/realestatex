from odoo.tests.common import TransactionCase
from odoo import fields

class TestTenantComplaint(TransactionCase):

    def setUp(self):
        super(TestTenantComplaint, self).setUp()

        # Create a user for assignment
        self.user_1 = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user1',
            'email': 'user1@example.com',
        })
        
        self.user_2 = self.env['res.users'].create({
            'name': 'User 2',
            'login': 'user2',
            'email': 'user2@example.com',
        })

        # Create a complaint type
        self.type_id = self.env['complaint.type'].create({
            'name': 'Noise Complaint'
        })

    def test_create_complaint(self):
        """ Test creating a tenant complaint and auto-assigning a user. """
        complaint = self.env['tenant.complaint'].create({
            'tenant_name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'address': '1234 Elm Street',
            'description': 'Loud noise during the night.',
            'type_id': self.type_id.id,
        })

        # Check if the complaint was created successfully
        self.assertEqual(complaint.tenant_name, 'John Doe')
        self.assertEqual(complaint.email, 'john.doe@example.com')
        self.assertEqual(complaint.description, 'Loud noise during the night.')

        # Check if an assignee is assigned
        self.assertTrue(complaint.assignee_id)


