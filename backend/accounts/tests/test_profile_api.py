from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Patient, User


class PatientProfileApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("profile@test.mx", "demo1234", role=User.Role.PATIENT)
        Patient.objects.create(user=self.user, first_name="Ana", last_name="Pérez")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_patient_can_update_own_contact_information(self):
        response = self.client.patch(
            "/api/v1/auth/profile", {"phone": "5550001122", "emergencyContactName": "Luis Pérez"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["phone"], "5550001122")
        self.assertEqual(response.data["emergencyContactName"], "Luis Pérez")
