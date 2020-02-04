from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Staff

from staff.serializers import StaffSerializer


STAFFS_URL = reverse('staff:staff-list')


class PublicStaffsAPITests(TestCase):
    """Test the publicly available staffs API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_staffs(self):
        """Test retrieving the tags"""
        Staff.objects.create(name='Topan', address='Pondok Pinang',
                             contact='087739991234', NIP='123456789')
        Staff.objects.create(name='Rizki', address='Parung Panjang',
                             contact='087739991234', NIP='432112345678')

        res = self.client.get(STAFFS_URL)

        staffs = Staff.objects.all().order_by('-name')
        serializer = StaffSerializer(staffs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_staff_successful(self):
        """Test creating a new staff"""
        payload = {
            'name': 'Topan',
            'address': 'Pondok Pinang',
            'contact': '087739991234',
            'NIP': '1234567890'
        }

        self.client.post(STAFFS_URL, payload)

        exists = Staff.objects.filter(
            name=payload['name'],
            NIP=payload['NIP']
        ).exists()

        self.assertTrue(exists)

    def test_create_staff_invalid(self):
        """Test creating a new staff with invalid payload"""
        payload = {
            'name': '',
            'address': '',
            'contact': '087739991234',
            'NIP': '1234567890'
        }

        res = self.client.post(STAFFS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
