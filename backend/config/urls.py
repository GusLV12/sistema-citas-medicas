from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """Una comprobación ligera para el proxy y las probes del despliegue."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({"status": "ok"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health", HealthView.as_view()),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/", include("catalogs.urls")),
    path("api/v1/", include("scheduling.urls")),
    path("api/v1/", include("consultations.urls")),
]
