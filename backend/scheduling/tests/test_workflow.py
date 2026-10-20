from datetime import time
from django.db import DatabaseError, transaction
from django.test import TestCase
from accounts.models import Doctor, Patient, User
from catalogs.models import AvailabilityRule, Clinic, DoctorClinic, DoctorSpecialty, Specialty
from consultations.models import Consultation
from scheduling.models import Appointment
from scheduling.services import available_slots, create_appointment, transition

class SchedulingWorkflowTests(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user("patient@test.mx", "demo1234", role=User.Role.PATIENT)
        self.patient = Patient.objects.create(user=self.patient_user, first_name="Ana", last_name="Pérez")
        doctor_user = User.objects.create_user("doctor@test.mx", "demo1234", role=User.Role.DOCTOR)
        self.doctor = Doctor.objects.create(user=doctor_user, license_number="TEST-001", first_name="Luis", last_name="Mora")
        self.specialty = Specialty.objects.create(name="General")
        self.clinic = Clinic.objects.create(name="Central", address="Calle 1")
        DoctorSpecialty.objects.create(doctor=self.doctor, specialty=self.specialty)
        self.doctor_clinic = DoctorClinic.objects.create(doctor=self.doctor, clinic=self.clinic)
        for weekday in range(7):
            AvailabilityRule.objects.create(doctor_clinic=self.doctor_clinic, weekday=weekday, starts_at=time(8), ends_at=time(18), slot_minutes=30)

    def reserve(self, slot_id):
        return create_appointment(
            actor=self.patient_user, patient=self.patient, specialty_id=self.specialty.id,
            doctor_id=self.doctor.id, clinic_id=self.clinic.id, slot_id=slot_id,
        )

    def test_booking_rechecks_a_slot_and_rejects_a_duplicate(self):
        slot = available_slots(self.doctor.id, self.clinic.id)[0]
        appointment = self.reserve(slot["id"])
        self.assertEqual(appointment.status, Appointment.Status.CONFIRMED)
        with self.assertRaisesMessage(Exception, "horario acaba de ocuparse"):
            self.reserve(slot["id"])

    def test_postgresql_trigger_requires_completed_appointment_for_consultation(self):
        slot = available_slots(self.doctor.id, self.clinic.id)[0]
        appointment = self.reserve(slot["id"])
        with self.assertRaises(DatabaseError):
            with transaction.atomic():
                Consultation.objects.create(
                    appointment=appointment, started_at=appointment.starts_at, ended_at=appointment.ends_at,
                )
        transition(appointment, Appointment.Status.COMPLETED, self.doctor.user)
        consultation = Consultation.objects.create(
            appointment=appointment, started_at=appointment.starts_at, ended_at=appointment.ends_at,
        )
        self.assertEqual(consultation.appointment_id, appointment.id)
