from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from scheduling.models import Appointment
from scheduling.services import transition

from .models import Consultation


def record_consultation(*, actor, appointment_id, clinical_summary="", follow_up_at=None, started_at=None, ended_at=None):
    if actor.role != "doctor":
        raise PermissionDenied("Solo el médico asignado puede registrar una consulta.")
    with transaction.atomic():
        appointment = Appointment.objects.select_for_update().filter(pk=appointment_id).first()
        if not appointment or appointment.doctor.user_id != actor.id:
            raise PermissionDenied("No puedes registrar una consulta para esta cita.")
        if hasattr(appointment, "consultation"):
            raise ValidationError("La cita ya tiene una consulta registrada.")
        if appointment.status != Appointment.Status.CONFIRMED:
            raise ValidationError("Solo se puede registrar una consulta para una cita confirmada.")
        started_at = started_at or appointment.starts_at
        ended_at = ended_at or timezone.now()
        if ended_at <= started_at:
            raise ValidationError("La consulta debe terminar después de su inicio.")
        transition(appointment, Appointment.Status.COMPLETED, actor)
        return Consultation.objects.create(
            appointment=appointment, started_at=started_at, ended_at=ended_at,
            clinical_summary=clinical_summary, follow_up_at=follow_up_at,
        )
