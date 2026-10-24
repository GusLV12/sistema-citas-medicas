from datetime import time

from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import Doctor, Patient, User
from catalogs.models import AvailabilityRule, Clinic, DoctorClinic, DoctorSpecialty, Specialty
from scheduling.services import available_slots, create_appointment


class ConsultationApiTests(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user("patient-api@test.mx", "demo1234", role=User.Role.PATIENT)
        self.patient = Patient.objects.create(user=self.patient_user, first_name="Ana", last_name="Pérez")
        self.doctor_user = User.objects.create_user("doctor-api@test.mx", "demo1234", role=User.Role.DOCTOR)
        self.doctor = Doctor.objects.create(user=self.doctor_user, license_number="API-001", first_name="Luis", last_name="Mora")
        self.specialty = Specialty.objects.create(name="General API")
        self.clinic = Clinic.objects.create(name="Central API", address="Calle 1")
        doctor_clinic = DoctorClinic.objects.create(doctor=self.doctor, clinic=self.clinic)
        DoctorSpecialty.objects.create(doctor=self.doctor, specialty=self.specialty)
        for weekday in range(7):
            AvailabilityRule.objects.create(doctor_clinic=doctor_clinic, weekday=weekday, starts_at=time(8), ends_at=time(18), slot_minutes=30)
        slot = available_slots(self.doctor.id, self.clinic.id)[0]
        self.appointment = create_appointment(
            actor=self.patient_user, patient=self.patient, specialty_id=self.specialty.id,
            doctor_id=self.doctor.id, clinic_id=self.clinic.id, slot_id=slot["id"],
        )
        self.client = APIClient()

    def test_doctor_creates_consultation_and_completes_appointment_atomically(self):
        self.client.force_authenticate(self.doctor_user)
        response = self.client.post("/api/v1/consultations", {"appointmentId": str(self.appointment.id), "clinicalSummary": "Seguimiento sin incidencias."}, format="json")
        self.assertEqual(response.status_code, 201)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "completed")

    def test_patient_cannot_create_a_consultation(self):
        self.client.force_authenticate(self.patient_user)
        response = self.client.post("/api/v1/consultations", {"appointmentId": str(self.appointment.id), "clinicalSummary": "Intento inválido."}, format="json")
        self.assertEqual(response.status_code, 403)
