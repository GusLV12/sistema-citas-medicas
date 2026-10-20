from django.urls import path
from .views import ConsultationCreateView
urlpatterns = [path("consultations", ConsultationCreateView.as_view())]
