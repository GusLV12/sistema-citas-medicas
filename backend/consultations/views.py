from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ConsultationSerializer
from .services import record_consultation

class ConsultationCreateView(APIView):
    def post(self, request):
        serializer = ConsultationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consultation = record_consultation(actor=request.user, **serializer.validated_data)
        return Response(ConsultationSerializer(consultation).data, status=201)
