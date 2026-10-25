from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdminDoctorViewSet, AdminUserViewSet, CsrfView, LoginView, LogoutView, MeView, PatientProfileView, RefreshView, RegisterView

router = DefaultRouter()
router.register("admin/users", AdminUserViewSet)
router.register("admin/doctors", AdminDoctorViewSet)

urlpatterns = [
    path("csrf", CsrfView.as_view()),
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("refresh", RefreshView.as_view()),
    path("me", MeView.as_view()),
    path("profile", PatientProfileView.as_view()),
    path("", include(router.urls)),
]
