# Generated manually to keep notification history independent from appointment history.
import uuid

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("scheduling", "0002_postgresql_integrity"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("kind", models.CharField(choices=[("booked", "Cita creada"), ("cancelled", "Cita cancelada"), ("rescheduled", "Cita reprogramada"), ("completed", "Cita completada"), ("no_show", "Inasistencia"), ("reminder_24h", "Recordatorio de 24 horas"), ("reminder_2h", "Recordatorio de 2 horas")], max_length=20)),
                ("title", models.CharField(max_length=160)),
                ("body", models.CharField(max_length=500)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("appointment", models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name="notifications", to="scheduling.appointment")),
                ("recipient", models.ForeignKey(on_delete=models.CASCADE, related_name="notifications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddConstraint(
            model_name="notification",
            constraint=models.UniqueConstraint(condition=models.Q(("appointment__isnull", False)), fields=("recipient", "appointment", "kind"), name="notification_recipient_appointment_kind_unique"),
        ),
    ]
