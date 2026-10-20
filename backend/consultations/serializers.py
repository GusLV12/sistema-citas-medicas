from rest_framework import serializers
from .models import Consultation

class ConsultationSerializer(serializers.ModelSerializer):
    appointmentId = serializers.UUIDField(source="appointment_id")
    clinicalSummary = serializers.CharField(source="clinical_summary", allow_blank=True)
    followUpAt = serializers.DateTimeField(source="follow_up_at", required=False, allow_null=True)
    class Meta:
        model = Consultation
        fields = ("id", "appointmentId", "clinicalSummary", "followUpAt", "started_at", "ended_at")
        extra_kwargs = {"started_at": {"required": False}, "ended_at": {"required": False}}
