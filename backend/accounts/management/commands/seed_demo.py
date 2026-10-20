from datetime import time
from django.core.management.base import BaseCommand
from accounts.models import Doctor, Patient, User
from catalogs.models import AvailabilityRule, Clinic, DoctorClinic, DoctorSpecialty, Specialty

class Command(BaseCommand):
    help = "Crea datos de demostración para paciente, médico, administración y disponibilidad."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(email="admin@salud.mx", defaults={"role": "admin"})
        admin.set_password("demo1234"); admin.save()
        patient_user, _ = User.objects.get_or_create(email="paciente@salud.mx", defaults={"role": "patient"})
        patient_user.set_password("demo1234"); patient_user.save()
        Patient.objects.get_or_create(user=patient_user, defaults={"first_name": "Ana", "last_name": "López"})
        doctor_user, _ = User.objects.get_or_create(email="medico@salud.mx", defaults={"role": "doctor"})
        doctor_user.set_password("demo1234"); doctor_user.save()
        doctor, _ = Doctor.objects.get_or_create(user=doctor_user, defaults={"license_number": "CED-001", "first_name": "Sofía", "last_name": "Ramos"})
        specialty, _ = Specialty.objects.get_or_create(name="Medicina general", defaults={"description": "Atención médica general"})
        clinic, _ = Clinic.objects.get_or_create(name="Clínica Central", defaults={"address": "Av. Principal 100"})
        DoctorSpecialty.objects.get_or_create(doctor=doctor, specialty=specialty)
        doctor_clinic, _ = DoctorClinic.objects.get_or_create(doctor=doctor, clinic=clinic)
        for weekday in range(5):
            AvailabilityRule.objects.get_or_create(doctor_clinic=doctor_clinic, weekday=weekday, starts_at=time(9), ends_at=time(14), defaults={"slot_minutes": 30})
        self.stdout.write(self.style.SUCCESS("Datos de demostración creados. Contraseña: demo1234"))
