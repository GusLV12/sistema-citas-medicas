from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Doctor, User


class AdminApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin-api@test.mx", "demo1234", role=User.Role.ADMIN)
        self.client = APIClient()
        self.client.force_authenticate(self.admin)

    def test_admin_creates_doctor_with_required_profile(self):
        response = self.client.post("/api/v1/auth/admin/doctors/", {
            "email": "new-doctor@test.mx", "password": "segura123", "firstName": "María",
            "lastName": "López", "licenseNumber": "CED-001",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        doctor = Doctor.objects.get(user__email="new-doctor@test.mx")
        self.assertEqual(doctor.user.role, User.Role.DOCTOR)

    def test_admin_can_create_another_administrator_only(self):
        response = self.client.post("/api/v1/auth/admin/users/", {
            "email": "new-admin@test.mx", "password": "segura123", "role": "admin",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="new-admin@test.mx", role=User.Role.ADMIN).exists())
