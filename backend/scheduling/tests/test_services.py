import uuid
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from scheduling.models import Appointment
from scheduling.serializers import AppointmentInputSerializer
from scheduling.services import patient_can_change

class AppointmentRuleTests(TestCase):
    def test_patient_can_change_only_with_24_hours(self):
        appointment = Appointment(starts_at=timezone.now() + timedelta(hours=24, seconds=1))
        self.assertTrue(patient_can_change(appointment))
        appointment.starts_at = timezone.now() + timedelta(hours=23, minutes=59)
        self.assertFalse(patient_can_change(appointment))


class AppointmentInputSerializerTests(TestCase):
    def test_api_camel_case_fields_map_to_service_arguments(self):
        payload = {
            "specialtyId": str(uuid.uuid4()),
            "doctorId": str(uuid.uuid4()),
            "clinicId": str(uuid.uuid4()),
            "slotId": "signed-slot",
            "reason": "Control anual",
        }

        serializer = AppointmentInputSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            set(serializer.validated_data),
            {"specialty_id", "doctor_id", "clinic_id", "slot_id", "reason"},
        )
