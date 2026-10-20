from rest_framework import serializers
from accounts.models import Doctor
from .models import AvailabilityRule, Clinic, ConsultingRoom, DoctorClinic, DoctorSpecialty, Specialty, Unavailability

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "name", "description", "is_active")

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ("id", "name", "address", "phone", "timezone", "is_active")

class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="full_name", read_only=True)
    specialtyIds = serializers.SerializerMethodField()
    clinicIds = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ("id", "name", "license_number", "biography", "is_active", "specialtyIds", "clinicIds")
    def get_specialtyIds(self, doctor): return [str(item.specialty_id) for item in doctor.doctor_specialties.all()]
    def get_clinicIds(self, doctor): return [str(item.clinic_id) for item in doctor.doctor_clinics.filter(is_active=True)]

class ConsultingRoomSerializer(serializers.ModelSerializer):
    class Meta: model = ConsultingRoom; fields = "__all__"
class DoctorSpecialtySerializer(serializers.ModelSerializer):
    class Meta: model = DoctorSpecialty; fields = "__all__"
class DoctorClinicSerializer(serializers.ModelSerializer):
    class Meta: model = DoctorClinic; fields = "__all__"
class AvailabilityRuleSerializer(serializers.ModelSerializer):
    class Meta: model = AvailabilityRule; fields = "__all__"
class UnavailabilitySerializer(serializers.ModelSerializer):
    class Meta: model = Unavailability; fields = "__all__"
