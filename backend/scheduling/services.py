from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, time, timedelta
import json
from zoneinfo import ZoneInfo
from django.core import signing
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from accounts.models import Patient
from catalogs.models import AvailabilityRule, DoctorClinic, DoctorSpecialty, Unavailability
from .models import Appointment, AppointmentStatusHistory

ACTIVE_STATUSES = (Appointment.Status.PENDING, Appointment.Status.CONFIRMED)
ZONE = ZoneInfo("America/Mexico_City")

def _encode_slot(doctor_id, clinic_id, starts_at, ends_at):
    payload = {"doctorId": str(doctor_id), "clinicId": str(clinic_id), "startsAt": starts_at.isoformat(), "endsAt": ends_at.isoformat()}
    return signing.dumps(payload, salt="appointment-slot", compress=True)

def decode_slot(slot_id):
    try:
        data = signing.loads(slot_id, salt="appointment-slot", max_age=3600)
        return data, datetime.fromisoformat(data["startsAt"]), datetime.fromisoformat(data["endsAt"])
    except Exception as exc:
        raise ValidationError({"slotId": "El horario ya no es válido. Actualiza la disponibilidad."}) from exc

def _overlaps(doctor_id, patient_id, starts_at, ends_at):
    period = Q(starts_at__lt=ends_at, ends_at__gt=starts_at, status__in=ACTIVE_STATUSES)
    return Appointment.objects.filter(period).filter(Q(doctor_id=doctor_id) | Q(patient_id=patient_id)).exists()

def _is_rule_available(doctor_clinic, starts_at, ends_at):
    local_start = starts_at.astimezone(ZONE)
    rules = AvailabilityRule.objects.filter(doctor_clinic=doctor_clinic, weekday=local_start.weekday(), is_active=True)
    for rule in rules:
        if rule.valid_from and local_start.date() < rule.valid_from: continue
        if rule.valid_until and local_start.date() > rule.valid_until: continue
        local_end = ends_at.astimezone(ZONE)
        if rule.starts_at <= local_start.time() and local_end.time() <= rule.ends_at and ends_at - starts_at == timedelta(minutes=rule.slot_minutes):
            return True
    return False

def available_slots(doctor_id, clinic_id, days=14):
    doctor_clinic = DoctorClinic.objects.filter(doctor_id=doctor_id, clinic_id=clinic_id, is_active=True).first()
    if not doctor_clinic:
        return []
    now = timezone.now()
    result = []
    rules = AvailabilityRule.objects.filter(doctor_clinic=doctor_clinic, is_active=True)
    for offset in range(days):
        date = (now.astimezone(ZONE) + timedelta(days=offset)).date()
        for rule in rules.filter(weekday=date.weekday()):
            if rule.valid_from and date < rule.valid_from: continue
            if rule.valid_until and date > rule.valid_until: continue
            current = datetime.combine(date, rule.starts_at, tzinfo=ZONE)
            limit = datetime.combine(date, rule.ends_at, tzinfo=ZONE)
            while current + timedelta(minutes=rule.slot_minutes) <= limit:
                end = current + timedelta(minutes=rule.slot_minutes)
                busy = Appointment.objects.filter(doctor_id=doctor_id, status__in=ACTIVE_STATUSES, starts_at__lt=end, ends_at__gt=current).exists()
                blocked = Unavailability.objects.filter(doctor_clinic=doctor_clinic, starts_at__lt=end, ends_at__gt=current).exists()
                if current > now and not busy and not blocked:
                    result.append({"id": _encode_slot(doctor_id, clinic_id, current, end), "startsAt": current.isoformat(), "endsAt": end.isoformat(), "available": True})
                current = end
    return result

def transition(appointment, status, actor, reason=""):
    old = appointment.status
    appointment.status = status
    fields = ["status", "updated_at"]
    if status == Appointment.Status.CANCELLED:
        appointment.cancelled_at = timezone.now()
        appointment.cancelled_by_user = actor
        appointment.cancellation_reason = reason
        fields += ["cancelled_at", "cancelled_by_user", "cancellation_reason"]
    appointment.save(update_fields=fields)
    AppointmentStatusHistory.objects.create(appointment=appointment, old_status=old, new_status=status, changed_by_user=actor, reason=reason)
    return appointment

def create_appointment(*, actor, patient, specialty_id, doctor_id, clinic_id, slot_id, reason="", rescheduled_from=None):
    data, starts_at, ends_at = decode_slot(slot_id)
    if str(doctor_id) != data["doctorId"] or str(clinic_id) != data["clinicId"]:
        raise ValidationError("El horario no corresponde al médico o clínica seleccionados.")
    try:
        with transaction.atomic():
            doctor_clinic = DoctorClinic.objects.select_for_update().filter(doctor_id=doctor_id, clinic_id=clinic_id, is_active=True).first()
            if not doctor_clinic or not DoctorSpecialty.objects.filter(doctor_id=doctor_id, specialty_id=specialty_id).exists():
                raise ValidationError("El médico no atiende esta especialidad en la clínica seleccionada.")
            if not _is_rule_available(doctor_clinic, starts_at, ends_at):
                raise ValidationError("El horario no corresponde a una regla de disponibilidad activa.")
            if Unavailability.objects.filter(doctor_clinic=doctor_clinic, starts_at__lt=ends_at, ends_at__gt=starts_at).exists() or _overlaps(doctor_id, patient.id, starts_at, ends_at):
                raise ValidationError("El horario acaba de ocuparse. Elige otra opción.")
            appointment = Appointment.objects.create(
                patient=patient, doctor_id=doctor_id, clinic_id=clinic_id, specialty_id=specialty_id,
                starts_at=starts_at, ends_at=ends_at, reason=reason, rescheduled_from=rescheduled_from,
            )
            AppointmentStatusHistory.objects.create(appointment=appointment, old_status=None, new_status=appointment.status, changed_by_user=actor)
            return appointment
    except IntegrityError as exc:
        raise ValidationError("El horario acaba de ocuparse. Elige otra opción.") from exc

def patient_can_change(appointment):
    return appointment.starts_at >= timezone.now() + timedelta(hours=24)
