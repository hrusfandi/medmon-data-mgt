from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Client
from client.serializers import ClientSerializer

from unittest.mock import patch


CLIENTS_URL = reverse('client:client-list')


class PrivateClientAPITests(TestCase):
    """Test the publicly available clients API"""

    def setUp(self):
        self.client = APIClient()

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_retrieve_clients(self, mock_jwt_auth):
        """Test retrieving the client objects"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        Client.objects.create(name='PT ABC', address='Jl.Jenderal Soedirman',
                              contact='021-999888')
        Client.objects.create(name='PT XYZ', address='Jl.Gatot Soebroto',
                              contact='021-888999')

        res = self.client.get(CLIENTS_URL)

        clients = Client.objects.all().order_by('-name')
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_create_client_successful(self, mock_jwt_auth):
        """Test creating client object successful"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        payload = {
            'name': 'PT ABC',
            'address': 'Jl. Jend Soedirman',
            'contact': '021-99998888'
        }

        res = self.client.post(CLIENTS_URL, payload)

        exists = Client.objects.filter(
            name=payload['name'],
            contact=payload['contact']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_create_client_invalid(self, mock_jwt_auth):
        """Test creating client with invalid payload"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        payload = {
            'name': '',
            'address': '',
            'contact': '02199998888'
        }

        res = self.client.post(CLIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
