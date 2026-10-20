from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from scheduling.models import Appointment
from scheduling.services import patient_can_change

class AppointmentRuleTests(TestCase):
    def test_patient_can_change_only_with_24_hours(self):
        appointment = Appointment(starts_at=timezone.now() + timedelta(hours=24, seconds=1))
        self.assertTrue(patient_can_change(appointment))
        appointment.starts_at = timezone.now() + timedelta(hours=23, minutes=59)
        self.assertFalse(patient_can_change(appointment))
