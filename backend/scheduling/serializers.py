from rest_framework import serializers
from .models import Appointment, Notification

class AppointmentSerializer(serializers.ModelSerializer):
    patientName = serializers.CharField(source="patient.full_name", read_only=True)
    doctorName = serializers.CharField(source="doctor.full_name", read_only=True)
    doctorId = serializers.UUIDField(source="doctor_id", read_only=True)
    specialty = serializers.CharField(source="specialty.name", read_only=True)
    clinic = serializers.CharField(source="clinic.name", read_only=True)
    startsAt = serializers.DateTimeField(source="starts_at", read_only=True)
    endsAt = serializers.DateTimeField(source="ends_at", read_only=True)
    canWriteConsultation = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = ("id", "patientName", "doctorName", "doctorId", "specialty", "clinic", "startsAt", "endsAt", "status", "reason", "cancellationReason", "canWriteConsultation")
    def get_canWriteConsultation(self, appointment):
        return appointment.status == Appointment.Status.CONFIRMED

    cancellationReason = serializers.CharField(source="cancellation_reason", read_only=True)

class AppointmentInputSerializer(serializers.Serializer):
    specialtyId = serializers.UUIDField()
    doctorId = serializers.UUIDField()
    clinicId = serializers.UUIDField()
    slotId = serializers.CharField()
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

class ActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=("cancel", "complete", "no_show"))
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)


class NotificationSerializer(serializers.ModelSerializer):
    appointmentId = serializers.UUIDField(source="appointment_id", allow_null=True, read_only=True)
    readAt = serializers.DateTimeField(source="read_at", allow_null=True, read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "appointmentId", "kind", "title", "body", "readAt", "createdAt")
