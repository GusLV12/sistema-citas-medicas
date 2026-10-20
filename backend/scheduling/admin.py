from django.contrib import admin
from .models import Appointment, AppointmentStatusHistory
admin.site.register(Appointment)
admin.site.register(AppointmentStatusHistory)
