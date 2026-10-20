from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/", include("catalogs.urls")),
    path("api/v1/", include("scheduling.urls")),
    path("api/v1/", include("consultations.urls")),
]
