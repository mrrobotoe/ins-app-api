"""
Tests for the models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized."""
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123',
                )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without an email raises error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='sample123',
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testpass123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_client(self):
        """Test creating a client."""
        user = get_user_model().objects.create(
            email='test@example.com',
            password='testpass123',
            name='Test User',
        )

        address = models.Address.objects.create(
            address='123 Test St',
            address_line_2='Apt 4B',
            city='Test City',
            state='Test State',
            zip_code='12345',
        )

        client = models.Client.objects.create(
            user=user,
            name='Test Client',
            main_address=address,
            phone_number='1234567890',
            email='client@example.com',
        )

        self.assertEqual(str(client), client.name)

    def test_create_inspection(self):
        """Test creating an inspection."""
        user = get_user_model().objects.create(
            email='test@example.com',
            password='testpass123',
            name='Test User',
        )

        address = models.Address.objects.create(
            address='123 Test St',
            address_line_2='Apt 4B',
            city='Test City',
            state='Test State',
            zip_code='12345',
        )

        client = models.Client.objects.create(
            user=user,
            name='Test Client',
            main_address=address,
            phone_number='1234567890',
            email='client@example.com',
        )

        inspection = models.Inspection.objects.create(
            inspector_name=user,
            client=client,
            inspection_date='2023-10-01',
            inspection_type='Residential',
            report_number='RPT-001',
            address=address,
            buyer_agent='John Doe',
            fee=100.00,
            payment_status='Paid',
            signed_status='Signed',
            release_status='Released',
            notes='Test notes',
        )

        self.assertEqual(str(inspection), f"{inspection.inspection_type} - {inspection.client.name}")
