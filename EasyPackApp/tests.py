from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from .models import Contact

class ContactTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.contact_url = reverse('contact')

    @patch('EasyPackApp.views.send_contact_emails')
    def test_contact_submission_success(self, mock_send_contact_emails):
        mock_send_contact_emails.return_value = {'admin_sent': True, 'customer_sent': True}
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '+91 9876543210',
            'subject': 'Box Enquiry',
            'message': 'Hello, I want to inquire about custom printed corrugated boxes.'
        }
        response = self.client.post(self.contact_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'johndoe@example.com')
        self.assertEqual(contact.phone_number, '+91 9876543210')
        self.assertEqual(contact.subject, 'Box Enquiry')
        self.assertEqual(contact.message, 'Hello, I want to inquire about custom printed corrugated boxes.')

        # Ensure email function was called with right arguments including phone_number
        mock_send_contact_emails.assert_called_once_with(
            name='John Doe',
            email='johndoe@example.com',
            phone_number='+91 9876543210',
            subject='Box Enquiry',
            message='Hello, I want to inquire about custom printed corrugated boxes.'
        )

    def test_contact_submission_invalid(self):
        # Missing required fields
        data = {
            'name': '',
            'email': 'not-an-email',
            'subject': '',
            'message': ''
        }
        response = self.client.post(self.contact_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('name', response.data)
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_list(self):
        Contact.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            phone_number='9876543210',
            subject='Pricing info',
            message='Need price quote.'
        )
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Jane Doe')
        self.assertEqual(response.data[0]['phone_number'], '9876543210')

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_utils_email_sending(self, mock_send):
        from .utils import send_contact_emails
        res = send_contact_emails(
            name='Test User',
            email='user@test.com',
            phone_number='+91 9876543210',
            subject='General Query',
            message='Testing email delivery'
        )
        self.assertTrue(res['admin_sent'])
        self.assertTrue(res['customer_sent'])
        self.assertEqual(mock_send.call_count, 2)
