from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Patient, User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "name", "email", "role")
    def get_name(self, user):
        profile = getattr(user, "patient_profile", None) or getattr(user, "doctor_profile", None)
        return profile.full_name if profile else user.email

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_name(self, value):
        if len(value.strip().split(maxsplit=1)) != 2:
            raise serializers.ValidationError("Escribe nombre y apellido.")
        return value

    def create(self, validated_data):
        first_name, last_name = validated_data.pop("name").strip().split(maxsplit=1)
        user = User.objects.create_user(role=User.Role.PATIENT, **validated_data)
        Patient.objects.create(user=user, first_name=first_name, last_name=last_name)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user or not user.is_active:
            raise serializers.ValidationError("Correo o contraseña inválidos.")
        attrs["user"] = user
        return attrs
