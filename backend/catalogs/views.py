from rest_framework import generics, viewsets
from accounts.models import Doctor
from accounts.permissions import IsAdmin
from .models import AvailabilityRule, Clinic, ConsultingRoom, DoctorClinic, DoctorSpecialty, Specialty, Unavailability
from .serializers import AvailabilityRuleSerializer, ClinicSerializer, ConsultingRoomSerializer, DoctorClinicSerializer, DoctorSerializer, DoctorSpecialtySerializer, SpecialtySerializer, UnavailabilitySerializer

class PublicSpecialtyList(generics.ListAPIView):
    permission_classes = []
    queryset = Specialty.objects.filter(is_active=True).order_by("name")
    serializer_class = SpecialtySerializer

class PublicClinicList(generics.ListAPIView):
    permission_classes = []
    queryset = Clinic.objects.filter(is_active=True).order_by("name")
    serializer_class = ClinicSerializer

class PublicDoctorList(generics.ListAPIView):
    permission_classes = []
    serializer_class = DoctorSerializer
    def get_queryset(self):
        queryset = Doctor.objects.filter(is_active=True).prefetch_related("doctor_specialties", "doctor_clinics")
        specialty_id, clinic_id = self.request.query_params.get("specialtyId"), self.request.query_params.get("clinicId")
        if specialty_id: queryset = queryset.filter(doctor_specialties__specialty_id=specialty_id)
        if clinic_id: queryset = queryset.filter(doctor_clinics__clinic_id=clinic_id, doctor_clinics__is_active=True)
        return queryset.distinct().order_by("last_name", "first_name")

class AdminCatalogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]

class SpecialtyViewSet(AdminCatalogViewSet): queryset = Specialty.objects.all(); serializer_class = SpecialtySerializer
class ClinicViewSet(AdminCatalogViewSet): queryset = Clinic.objects.all(); serializer_class = ClinicSerializer
class ConsultingRoomViewSet(AdminCatalogViewSet): queryset = ConsultingRoom.objects.all(); serializer_class = ConsultingRoomSerializer
class DoctorSpecialtyViewSet(AdminCatalogViewSet): queryset = DoctorSpecialty.objects.all(); serializer_class = DoctorSpecialtySerializer
class DoctorClinicViewSet(AdminCatalogViewSet): queryset = DoctorClinic.objects.all(); serializer_class = DoctorClinicSerializer
class AvailabilityRuleViewSet(AdminCatalogViewSet): queryset = AvailabilityRule.objects.all(); serializer_class = AvailabilityRuleSerializer
class UnavailabilityViewSet(AdminCatalogViewSet): queryset = Unavailability.objects.all(); serializer_class = UnavailabilitySerializer
