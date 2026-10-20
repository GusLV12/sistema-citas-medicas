from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AvailabilityRuleViewSet, ClinicViewSet, ConsultingRoomViewSet, DoctorClinicViewSet, DoctorSpecialtyViewSet, PublicClinicList, PublicDoctorList, PublicSpecialtyList, SpecialtyViewSet, UnavailabilityViewSet

router = DefaultRouter()
router.register("admin/catalogs/specialties", SpecialtyViewSet)
router.register("admin/catalogs/clinics", ClinicViewSet)
router.register("admin/catalogs/rooms", ConsultingRoomViewSet)
router.register("admin/catalogs/doctor-specialties", DoctorSpecialtyViewSet)
router.register("admin/catalogs/doctor-clinics", DoctorClinicViewSet)
router.register("admin/catalogs/availability-rules", AvailabilityRuleViewSet)
router.register("admin/catalogs/unavailabilities", UnavailabilityViewSet)

urlpatterns = [
    path("specialties", PublicSpecialtyList.as_view()),
    path("clinics", PublicClinicList.as_view()),
    path("doctors", PublicDoctorList.as_view()),
    path("", include(router.urls)),
]
