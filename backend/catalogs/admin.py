from django.contrib import admin
from .models import AvailabilityRule, Clinic, ConsultingRoom, DoctorClinic, DoctorSpecialty, Specialty, Unavailability
admin.site.register([Specialty, Clinic, ConsultingRoom, DoctorSpecialty, DoctorClinic, AvailabilityRule, Unavailability])
