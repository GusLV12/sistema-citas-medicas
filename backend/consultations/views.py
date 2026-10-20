from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from scheduling.models import Appointment
from scheduling.services import transition
from .models import Consultation
from .serializers import ConsultationSerializer

class ConsultationCreateView(APIView):
    def post(self, request):
        if request.user.role != "doctor":
            raise PermissionDenied("Solo el médico asignado puede registrar una consulta.")
        serializer = ConsultationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment_id = serializer.validated_data["appointment_id"]
        with transaction.atomic():
            appointment = Appointment.objects.select_for_update().filter(pk=appointment_id).first()
            if not appointment or appointment.doctor.user_id != request.user.id:
                raise PermissionDenied("No puedes registrar una consulta para esta cita.")
            if hasattr(appointment, "consultation"):
                raise ValidationError("La cita ya tiene una consulta registrada.")
            if appointment.status != Appointment.Status.CONFIRMED:
                raise ValidationError("Solo se puede registrar una consulta para una cita confirmada.")
            started_at = serializer.validated_data.get("started_at", appointment.starts_at)
            ended_at = serializer.validated_data.get("ended_at", timezone.now())
            if ended_at <= started_at:
                raise ValidationError("La consulta debe terminar después de su inicio.")
            transition(appointment, Appointment.Status.COMPLETED, request.user)
            consultation = Consultation.objects.create(
                appointment=appointment, started_at=started_at, ended_at=ended_at,
                clinical_summary=serializer.validated_data.get("clinical_summary", ""),
                follow_up_at=serializer.validated_data.get("follow_up_at"),
            )
        return Response(ConsultationSerializer(consultation).data, status=201)
