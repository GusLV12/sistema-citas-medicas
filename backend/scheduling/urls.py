from django.urls import path
from .views import AppointmentDetailView, AppointmentListCreateView, AvailabilityView, NotificationListView, NotificationReadAllView, NotificationReadView, RescheduleView
urlpatterns = [
    path("availability", AvailabilityView.as_view()),
    path("appointments", AppointmentListCreateView.as_view()),
    path("appointments/<uuid:pk>", AppointmentDetailView.as_view()),
    path("appointments/<uuid:pk>/reschedule", RescheduleView.as_view()),
    path("notifications", NotificationListView.as_view()),
    path("notifications/read-all", NotificationReadAllView.as_view()),
    path("notifications/<uuid:pk>/read", NotificationReadView.as_view()),
]
