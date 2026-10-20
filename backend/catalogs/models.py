import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from accounts.models import Doctor

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Specialty(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Clinic(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=160)
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True)
    timezone = models.CharField(max_length=64, default="America/Mexico_City")
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class ConsultingRoom(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name="rooms")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=("clinic", "code"), name="room_clinic_code_unique")]
    def __str__(self): return f"{self.clinic} · {self.code}"

class DoctorSpecialty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="doctor_specialties")
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name="doctor_specialties")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=("doctor", "specialty"), name="doctor_specialty_unique")]

class DoctorClinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="doctor_clinics")
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name="doctor_clinics")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=("doctor", "clinic"), name="doctor_clinic_unique")]

class AvailabilityRule(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_clinic = models.ForeignKey(DoctorClinic, on_delete=models.CASCADE, related_name="availability_rules")
    weekday = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6)])
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    slot_minutes = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(5), MaxValueValidator(240)])
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(starts_at__lt=models.F("ends_at")), name="availability_period_valid"),
            models.CheckConstraint(condition=models.Q(valid_until__isnull=True) | models.Q(valid_from__isnull=True) | models.Q(valid_from__lte=models.F("valid_until")), name="availability_dates_valid"),
        ]

class Unavailability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_clinic = models.ForeignKey(DoctorClinic, on_delete=models.CASCADE, related_name="unavailabilities")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    reason = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(starts_at__lt=models.F("ends_at")), name="unavailability_period_valid")]
