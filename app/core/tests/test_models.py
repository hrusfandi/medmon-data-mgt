from django.test import TestCase
from core import models


class ModelTests(TestCase):

    def test_client_str(self):
        """Test the client string representation"""
        client = models.Client.objects.create(
            name='PT. ABC',
            address='Jalan Jenderal Soedirman, Kav.41, Jakarta Pusat',
            contact='021-556557'
        )

        self.assertEqual(str(client), client.name)

    def test_staff_str(self):
        """Test the staff string representation"""
        staff = models.Staff.objects.create(
            name='Topan Febriansyah',
            contact='089912345678',
            address='Pondok Pinang',
            NIP='1234567898765432'
        )

        self.assertEqual(str(staff), staff.name)
