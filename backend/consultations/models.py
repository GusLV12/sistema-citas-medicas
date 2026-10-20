import uuid
from django.db import models
from scheduling.models import Appointment

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT, related_name="consultation")
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    clinical_summary = models.TextField(blank=True)
    follow_up_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(started_at__lt=models.F("ended_at")), name="consultation_period_valid")]
