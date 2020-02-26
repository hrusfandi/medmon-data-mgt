from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch

from core.models import Staff

from staff.serializers import StaffSerializer

STAFFS_URL = reverse('staff:staff-list')


class PublicStaffsAPITests(TestCase):
    """Test the publicly available staffs API"""

    def setUp(self):
        self.client = APIClient()


class PrivateStaffAPITest(TestCase):
    """Test private access of staff api"""

    def setUp(self):
        self.client = APIClient()

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_retrieve_staffs(self, mock_jwt_auth):
        """Test retrieving the tags"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        Staff.objects.create(name='Topan', address='Pondok Pinang',
                             contact='087739991234', NIP='123456789')
        Staff.objects.create(name='Rizki', address='Parung Panjang',
                             contact='087739991234', NIP='432112345678')

        res = self.client.get(STAFFS_URL)

        staffs = Staff.objects.all().order_by('-name')
        serializer = StaffSerializer(staffs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_create_staff_successful(self, mock_jwt_auth):
        """Test creating a new staff"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

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

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_create_staff_invalid(self, mock_jwt_auth):
        """Test creating a new staff with invalid payload"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        payload = {
            'name': '',
            'address': '',
            'contact': '087739991234',
            'NIP': '1234567890'
        }

        res = self.client.post(STAFFS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
