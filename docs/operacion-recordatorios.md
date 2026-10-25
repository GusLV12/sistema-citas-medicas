# Recordatorios internos

La aplicación crea notificaciones al reservar, cancelar, reprogramar, completar o registrar una inasistencia. Los recordatorios de 24 horas y 2 horas se generan dentro de la aplicación para el paciente y el médico asignado.

Ejecuta el siguiente comando cada 15 minutos desde el programador de tareas del entorno de despliegue:

```powershell
cd backend
.\.venv\Scripts\python manage.py create_appointment_reminders
```

El comando es idempotente: una restricción de base de datos impide crear el mismo recordatorio dos veces para la misma cita y destinatario.
