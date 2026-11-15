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
    def validate(self, attrs):
        starts_at = attrs.get("starts_at", getattr(self.instance, "starts_at", None))
        ends_at = attrs.get("ends_at", getattr(self.instance, "ends_at", None))
        if starts_at and ends_at and ends_at <= starts_at:
            raise serializers.ValidationError({"ends_at": "La hora final debe ser posterior a la hora inicial."})
        valid_from = attrs.get("valid_from", getattr(self.instance, "valid_from", None))
        valid_until = attrs.get("valid_until", getattr(self.instance, "valid_until", None))
        if valid_from and valid_until and valid_until < valid_from:
            raise serializers.ValidationError({"valid_until": "La vigencia final no puede ser anterior a la inicial."})
        return attrs
class UnavailabilitySerializer(serializers.ModelSerializer):
    class Meta: model = Unavailability; fields = "__all__"
    def validate(self, attrs):
        starts_at = attrs.get("starts_at", getattr(self.instance, "starts_at", None))
        ends_at = attrs.get("ends_at", getattr(self.instance, "ends_at", None))
        if starts_at and ends_at and ends_at <= starts_at:
            raise serializers.ValidationError({"ends_at": "El fin del bloqueo debe ser posterior a su inicio."})
        return attrs
