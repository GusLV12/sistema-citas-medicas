from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from .models import Doctor, Patient, User

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
        with transaction.atomic():
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


class AdminUserSerializer(UserSerializer):
    password = serializers.CharField(min_length=8, write_only=True, required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)

    class Meta(UserSerializer.Meta):
        fields = ("id", "name", "email", "role", "isActive", "password")
        read_only_fields = ("id", "name")

    def validate_role(self, value):
        if self.instance and value != self.instance.role:
            raise serializers.ValidationError("El rol no se puede cambiar cuando el usuario ya tiene perfil.")
        if not self.instance and value != User.Role.ADMIN:
            raise serializers.ValidationError("Los pacientes se registran públicamente y los médicos se crean desde /admin/doctors.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AdminDoctorSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True, required=False)
    firstName = serializers.CharField(source="first_name", max_length=100)
    lastName = serializers.CharField(source="last_name", max_length=100)
    licenseNumber = serializers.CharField(source="license_number", max_length=100)
    biography = serializers.CharField(required=False, allow_blank=True)
    isActive = serializers.BooleanField(source="is_active", required=False)
    defaultAppointmentMinutes = serializers.IntegerField(source="default_appointment_minutes", min_value=5, max_value=240, required=False)

    def validate(self, attrs):
        if not self.instance and "password" not in attrs:
            raise serializers.ValidationError({"password": "La contraseña es obligatoria al crear un médico."})
        return attrs

    def to_representation(self, doctor):
        return {
            "id": str(doctor.id), "email": doctor.user.email,
            "firstName": doctor.first_name, "lastName": doctor.last_name,
            "licenseNumber": doctor.license_number, "biography": doctor.biography,
            "isActive": doctor.is_active, "defaultAppointmentMinutes": doctor.default_appointment_minutes,
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        with transaction.atomic():
            user = User.objects.create_user(email=email, password=password, role=User.Role.DOCTOR)
            return Doctor.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        if email:
            instance.user.email = email
        if password:
            instance.user.set_password(password)
        if email or password:
            instance.user.save()
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
