"""
Tests for the Client API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Client

from client.serializers import ClientSerializer

CLIENTS_URL = reverse('client:client-list')


def create_client(user, **params):
    """
    Create a client with the given parameters.
    """
    defaults = {
        'name': 'Test Client',
        'email': 'client@example.com',
        'phone_number': '1234567890',
        'main_address': '123 Main St',
    }
    defaults.update(params)

    client = Client.objects.create(user=user, **defaults)
    return client


class PublicClientAPITests(TestCase):
    """
    Test the publicly available client API.
    """

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """
        Test that authentication is required to access the client API.
        """
        res = self.client.get(CLIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClientAPITests(TestCase):
    """
    Test the private client API.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_clients(self):
        """
        Test retrieving a list of clients.
        """
        create_client(user=self.user)
        create_client(user=self.user)

        res = self.client.get(CLIENTS_URL)

        clients = Client.objects.all().order_by('-id')
        serializer = ClientSerializer(clients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_client_list_limited_to_user(self):
        """
        Test that clients returned are for the authenticated user.
        """
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='testpass123',
            name='Other User',
        )
        create_client(user=other_user)
        create_client(user=self.user)

        res = self.client.get(CLIENTS_URL)

        clients = Client.objects.filter(user=self.user)
        serializer = ClientSerializer(clients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
