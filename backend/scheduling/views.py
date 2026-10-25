from datetime import datetime, time
from zoneinfo import ZoneInfo
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment, Notification
from .serializers import ActionSerializer, AppointmentInputSerializer, AppointmentSerializer, NotificationSerializer
from .services import available_slots, create_appointment, patient_can_change, transition

ACTIVE_STATUSES = (Appointment.Status.PENDING, Appointment.Status.CONFIRMED)
ZONE = ZoneInfo("America/Mexico_City")

class AvailabilityView(APIView):
    permission_classes = []
    def get(self, request):
        doctor_id, clinic_id = request.query_params.get("doctorId"), request.query_params.get("clinicId")
        if not doctor_id or not clinic_id:
            raise ValidationError("doctorId y clinicId son obligatorios.")
        return Response(available_slots(doctor_id, clinic_id))

class AppointmentListCreateView(APIView):
    def get(self, request):
        queryset = Appointment.objects.select_related("patient", "doctor", "clinic", "specialty")
        if request.user.role == "patient":
            queryset = queryset.filter(patient=request.user.patient_profile)
        elif request.user.role == "doctor":
            queryset = queryset.filter(doctor=request.user.doctor_profile)
        start_date = request.query_params.get("from") or request.query_params.get("date")
        end_date = request.query_params.get("to") or request.query_params.get("date")
        try:
            if start_date:
                start = timezone.make_aware(datetime.combine(datetime.fromisoformat(start_date).date(), time.min), ZONE)
                queryset = queryset.filter(starts_at__gte=start)
            if end_date:
                end = timezone.make_aware(datetime.combine(datetime.fromisoformat(end_date).date(), time.max), ZONE)
                queryset = queryset.filter(starts_at__lte=end)
        except ValueError as exc:
            raise ValidationError({"date": "Usa una fecha ISO (AAAA-MM-DD)."}) from exc
        status_filter = request.query_params.get("status")
        if status_filter:
            allowed = {item[0] for item in Appointment.Status.choices}
            statuses = status_filter.split(",")
            if not set(statuses).issubset(allowed):
                raise ValidationError({"status": "Estado de cita inválido."})
            queryset = queryset.filter(status__in=statuses)
        return Response(AppointmentSerializer(queryset, many=True).data)

    def post(self, request):
        if request.user.role != "patient":
            raise PermissionDenied("Solo pacientes pueden reservar citas.")
        serializer = AppointmentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = create_appointment(actor=request.user, patient=request.user.patient_profile, **serializer.validated_data)
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)

class AppointmentDetailView(APIView):
    def get_object(self, request, pk):
        appointment = Appointment.objects.select_related("patient", "doctor", "clinic", "specialty").filter(pk=pk).first()
        if not appointment:
            raise NotFound()
        if request.user.role == "patient" and appointment.patient.user_id != request.user.id:
            raise PermissionDenied()
        if request.user.role == "doctor" and appointment.doctor.user_id != request.user.id:
            raise PermissionDenied()
        return appointment

    def get(self, request, pk):
        return Response(AppointmentSerializer(self.get_object(request, pk)).data)

    def patch(self, request, pk):
        appointment = self.get_object(request, pk)
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data["action"]
        reason = serializer.validated_data.get("reason", "")
        if appointment.status not in ACTIVE_STATUSES:
            raise ValidationError("Solo se pueden modificar citas activas.")
        if action == "cancel":
            if request.user.role == "patient" and not patient_can_change(appointment):
                raise ValidationError("Las cancelaciones requieren al menos 24 horas de anticipación.")
            if request.user.role == "doctor" and appointment.doctor.user_id != request.user.id:
                raise PermissionDenied()
            if request.user.role not in ("patient", "doctor", "admin"):
                raise PermissionDenied()
            transition(appointment, Appointment.Status.CANCELLED, request.user, reason)
        elif request.user.role == "doctor" and appointment.doctor.user_id == request.user.id:
            status_value = Appointment.Status.COMPLETED if action == "complete" else Appointment.Status.NO_SHOW
            transition(appointment, status_value, request.user, reason)
        else:
            raise PermissionDenied()
        return Response(AppointmentSerializer(appointment).data)

class RescheduleView(AppointmentDetailView):
    def post(self, request, pk):
        original = self.get_object(request, pk)
        if request.user.role != "patient" or original.patient.user_id != request.user.id:
            raise PermissionDenied()
        if original.status not in ACTIVE_STATUSES:
            raise ValidationError("Solo se pueden reprogramar citas activas.")
        if not patient_can_change(original):
            raise ValidationError("La reprogramación requiere al menos 24 horas de anticipación.")
        serializer = AppointmentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            original = Appointment.objects.select_for_update().get(pk=original.pk)
            if original.status not in ACTIVE_STATUSES:
                raise ValidationError("Solo se pueden reprogramar citas activas.")
            if not patient_can_change(original):
                raise ValidationError("La reprogramación requiere al menos 24 horas de anticipación.")
            replacement = create_appointment(actor=request.user, patient=original.patient, rescheduled_from=original, **serializer.validated_data)
            transition(original, Appointment.Status.RESCHEDULED, request.user)
        return Response(AppointmentSerializer(replacement).data, status=status.HTTP_201_CREATED)


class NotificationListView(APIView):
    def get(self, request):
        queryset = Notification.objects.filter(recipient=request.user)
        return Response({
            "results": NotificationSerializer(queryset, many=True).data,
            "unreadCount": queryset.filter(read_at__isnull=True).count(),
        })


class NotificationReadView(APIView):
    def patch(self, request, pk):
        notification = Notification.objects.filter(pk=pk, recipient=request.user).first()
        if not notification:
            raise NotFound()
        if notification.read_at is None:
            notification.read_at = timezone.now()
            notification.save(update_fields=["read_at"])
        return Response(NotificationSerializer(notification).data)


class NotificationReadAllView(APIView):
    def patch(self, request):
        Notification.objects.filter(recipient=request.user, read_at__isnull=True).update(read_at=timezone.now())
        return Response(status=status.HTTP_204_NO_CONTENT)
