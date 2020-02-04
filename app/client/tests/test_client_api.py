from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Client

from client.serializers import ClientSerializer


CLIENTS_URL = reverse('client:client-list')


class PublicClientsAPITests(TestCase):
    """Test the publicly available clients API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_clients(self):
        """Test retrieving the client objects"""
        Client.objects.create(name='PT ABC', address='Jl.Jenderal Soedirman',
                              contact='021-999888')
        Client.objects.create(name='PT XYZ', address='Jl.Gatot Soebroto',
                              contact='021-888999')

        res = self.client.get(CLIENTS_URL)

        clients = Client.objects.all().order_by('-name')
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_client_successful(self):
        """Test creating client object successful"""
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

    def test_create_client_invalid(self):
        """Test creating client with invalid payload"""
        payload = {
            'name': '',
            'address': '',
            'contact': '02199998888'
        }

        res = self.client.post(CLIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
