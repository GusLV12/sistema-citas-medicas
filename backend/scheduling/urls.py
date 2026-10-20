from django.urls import path
from .views import AppointmentDetailView, AppointmentListCreateView, AvailabilityView, RescheduleView
urlpatterns = [
    path("availability", AvailabilityView.as_view()),
    path("appointments", AppointmentListCreateView.as_view()),
    path("appointments/<uuid:pk>", AppointmentDetailView.as_view()),
    path("appointments/<uuid:pk>/reschedule", RescheduleView.as_view()),
]
