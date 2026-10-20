from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import enforce_csrf
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

AUTH_COOKIE_PATH = "/api/v1/"

def cookie_options(max_age):
    return {"httponly": True, "secure": settings.COOKIE_SECURE, "samesite": settings.COOKIE_SAMESITE, "max_age": max_age, "path": AUTH_COOKIE_PATH}

def set_auth_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    response.set_cookie("access_token", str(refresh.access_token), **cookie_options(900))
    response.set_cookie("refresh_token", str(refresh), **cookie_options(604800))
    return response

class CsrfView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def get(self, request):
        return Response({"csrfToken": get_token(request)})

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return set_auth_cookies(Response(UserSerializer(user).data, status=status.HTTP_201_CREATED), user)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return set_auth_cookies(Response(UserSerializer(serializer.validated_data["user"]).data), serializer.validated_data["user"])

class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        enforce_csrf(request)
        raw = request.COOKIES.get("refresh_token")
        if not raw:
            return Response({"message": "Sesión no disponible."}, status=401)
        try:
            refresh = RefreshToken(raw)
            response = Response({"detail": "Sesión renovada."})
            response.set_cookie("access_token", str(refresh.access_token), **cookie_options(900))
            if api_settings.ROTATE_REFRESH_TOKENS:
                refresh.set_jti()
                refresh.set_exp()
                refresh.set_iat()
                response.set_cookie("refresh_token", str(refresh), **cookie_options(604800))
            return response
        except Exception:
            return Response({"message": "Sesión no válida."}, status=401)

class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        if request.COOKIES.get("access_token") or request.COOKIES.get("refresh_token"):
            enforce_csrf(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access_token", path=AUTH_COOKIE_PATH)
        response.delete_cookie("refresh_token", path=AUTH_COOKIE_PATH)
        return response
