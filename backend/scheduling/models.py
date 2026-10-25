import uuid
from django.db import models
from accounts.models import Doctor, Patient, User
from catalogs.models import Clinic, ConsultingRoom, Specialty

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        CONFIRMED = "confirmed", "Confirmada"
        CANCELLED = "cancelled", "Cancelada"
        COMPLETED = "completed", "Completada"
        NO_SHOW = "no_show", "Inasistencia"
        RESCHEDULED = "rescheduled", "Reprogramada"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name="appointments")
    consulting_room = models.ForeignKey(ConsultingRoom, on_delete=models.PROTECT, null=True, blank=True, related_name="appointments")
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name="appointments")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.CONFIRMED)
    reason = models.CharField(max_length=500, blank=True)
    cancellation_reason = models.CharField(max_length=500, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="cancelled_appointments")
    rescheduled_from = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="rescheduled_to")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ("starts_at",)
        constraints = [
            models.CheckConstraint(condition=models.Q(starts_at__lt=models.F("ends_at")), name="appointment_period_valid"),
            models.CheckConstraint(condition=models.Q(rescheduled_from__isnull=True) | ~models.Q(rescheduled_from=models.F("id")), name="appointment_not_self_rescheduled"),
        ]

class AppointmentStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT, related_name="status_history")
    old_status = models.CharField(max_length=12, choices=Appointment.Status.choices, null=True, blank=True)
    new_status = models.CharField(max_length=12, choices=Appointment.Status.choices)
    changed_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    reason = models.CharField(max_length=500, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    """Aviso interno, sin información clínica sensible."""
    class Kind(models.TextChoices):
        BOOKED = "booked", "Cita creada"
        CANCELLED = "cancelled", "Cita cancelada"
        RESCHEDULED = "rescheduled", "Cita reprogramada"
        COMPLETED = "completed", "Cita completada"
        NO_SHOW = "no_show", "Inasistencia"
        REMINDER_24H = "reminder_24h", "Recordatorio de 24 horas"
        REMINDER_2H = "reminder_2h", "Recordatorio de 2 horas"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    appointment = models.ForeignKey(Appointment, null=True, blank=True, on_delete=models.SET_NULL, related_name="notifications")
    kind = models.CharField(max_length=20, choices=Kind.choices)
    title = models.CharField(max_length=160)
    body = models.CharField(max_length=500)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("recipient", "appointment", "kind"),
                condition=models.Q(appointment__isnull=False),
                name="notification_recipient_appointment_kind_unique",
            ),
        ]
