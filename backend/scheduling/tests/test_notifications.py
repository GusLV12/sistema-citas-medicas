from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import Doctor, Patient, User
from catalogs.models import Clinic, DoctorClinic, DoctorSpecialty, Specialty
from scheduling.models import Appointment, Notification
from scheduling.services import create_due_reminders, transition


class NotificationTests(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user("ana@notifications.mx", "demo1234", role=User.Role.PATIENT)
        self.patient = Patient.objects.create(user=self.patient_user, first_name="Ana", last_name="López")
        doctor_user = User.objects.create_user("luis@notifications.mx", "demo1234", role=User.Role.DOCTOR)
        self.doctor = Doctor.objects.create(user=doctor_user, license_number="NOT-001", first_name="Luis", last_name="Mora")
        self.specialty = Specialty.objects.create(name="Notificaciones")
        self.clinic = Clinic.objects.create(name="Clínica de avisos", address="Calle 1")
        DoctorClinic.objects.create(doctor=self.doctor, clinic=self.clinic)
        DoctorSpecialty.objects.create(doctor=self.doctor, specialty=self.specialty)
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, specialty=self.specialty, clinic=self.clinic,
            starts_at=timezone.now() + timedelta(days=2), ends_at=timezone.now() + timedelta(days=2, minutes=30),
        )

    def test_transition_notifies_only_appointment_participants(self):
        transition(self.appointment, Appointment.Status.CANCELLED, self.patient_user, "Cambio de plan")
        self.assertEqual(Notification.objects.filter(appointment=self.appointment, kind=Notification.Kind.CANCELLED).count(), 2)
        client = APIClient()
        client.force_authenticate(self.patient_user)
        response = client.get("/api/v1/notifications")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["unreadCount"], 1)
        self.assertEqual(response.data["results"][0]["appointmentId"], str(self.appointment.id))

    def test_reminder_command_is_idempotent(self):
        self.appointment.starts_at = timezone.now() + timedelta(hours=24)
        self.appointment.ends_at = self.appointment.starts_at + timedelta(minutes=30)
        self.appointment.save()
        first = create_due_reminders()
        second = create_due_reminders()
        self.assertEqual(first, 2)
        self.assertEqual(second, 0)
        self.assertEqual(Notification.objects.filter(kind=Notification.Kind.REMINDER_24H).count(), 2)
