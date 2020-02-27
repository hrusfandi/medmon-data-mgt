from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch

from core.models import Staff

from staff.serializers import StaffSerializer

STAFFS_URL = reverse('staff:staff-list')


def detail_url(staff_id):
    """Return staff's detail URL"""
    return reverse('staff:staff-detail', args=[staff_id])


def sample_staff(**params):
    """Create and return sample staff"""
    defaults = {
        'name': 'Test name',
        'address': 'test address',
        'contact': '089912345678',
        'NIP': '1234567890'
    }

    defaults.update(params)

    return Staff.objects.create(**defaults)


class PublicStaffsAPITests(TestCase):
    """Test the publicly available staffs API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_staffs_forbidden(self):
        """Test retrieving the staffs forbidden access"""
        Staff.objects.create(name='Topan', address='Pondok Pinang',
                             contact='087739991234', NIP='123456789')
        Staff.objects.create(name='Rizki', address='Parung Panjang',
                             contact='087739991234', NIP='432112345678')

        res = self.client.get(STAFFS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_staff_forbidden(self):
        """Test creating staff forbidden access"""
        payload = {
            'name': 'Topan',
            'address': 'Pondok Pinang',
            'contact': '087739991234',
            'NIP': '1234567890'
        }

        res = self.client.post(STAFFS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_retrieve_staff_detail(self, mock_jwt_auth):
        """Test viewing staff detail"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        staff = sample_staff()

        url = detail_url(staff.id)
        res = self.client.get(url)

        serializer = StaffSerializer(staff)
        self.assertEqual(res.data, serializer.data)

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_full_update_staff(self, mock_jwt_auth):
        """test updating staff"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        staff = sample_staff()

        payload = {
            'name': 'Hendi',
            'address': 'Tangerang',
            'contact': '087739271234',
            'NIP': '1234567890'
        }

        url = detail_url(staff.id)
        self.client.put(url, payload)

        staff.refresh_from_db()
        self.assertEqual(staff.name, payload['name'])
        self.assertEqual(staff.address, payload['address'])
        self.assertEqual(staff.contact, payload['contact'])
        self.assertEqual(staff.NIP, payload['NIP'])

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_partial_update_staff(self, mock_jwt_auth):
        """Test updating partial data of staff"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        staff = sample_staff()
        staff_address = staff.address

        payload = {
            'name': 'Hendi Rusfandi',
            'contact': '089912345678',
        }

        url = detail_url(staff.id)
        self.client.patch(url, payload)

        staff.refresh_from_db()
        self.assertEqual(staff.name, payload['name'])
        self.assertEqual(staff.contact, payload['contact'])
        self.assertEqual(staff.address, staff_address)

    @patch('core.authentication.JWTAuthentication.authenticate')
    def test_delete_staff(self, mock_jwt_auth):
        """Test deleting staff"""
        data = {"token_type": "access", "exp": 1582703472,
                "jti": "fcbaabbc963542429db9e93fd0aa158d", "user_id": 2}
        mock_jwt_auth.return_value = (data, None)

        staff = sample_staff(name='Hendi Rusfandi')

        url = detail_url(staff.id)
        self.client.delete(url)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
