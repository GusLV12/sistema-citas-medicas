# Arquitectura: sistema de citas médicas

## Alcance del MVP

El sistema permite a pacientes reservar citas con médicos, a médicos administrar su disponibilidad y a administradores configurar clínicas, especialidades y cuentas. La **cita** reserva un horario; la **consulta** registra la atención efectivamente realizada. Una cita cancelada o con inasistencia no genera una consulta.

## Entidades y relaciones

| Entidad | Responsabilidad |
|---|---|
| `users` | Acceso, rol, correo, contraseña cifrada y estado de cuenta. |
| `patients` / `doctors` | Perfiles asociados uno a uno con `users`. |
| `specialties` / `doctor_specialties` | Catálogo y capacidades profesionales de cada médico. |
| `clinics` / `consulting_rooms` | Sedes y consultorios físicos. |
| `doctor_clinics` | Sedes en las que atiende cada médico. |
| `availability_rules` / `unavailabilities` | Horario semanal y bloqueos puntuales. |
| `appointments` | Reserva de paciente, médico, sede, especialidad y periodo. |
| `consultations` | Registro opcional de una cita completada, uno a uno con ella. |
| `appointment_status_history` | Auditoría de cada cambio de estado. |

## Flujo de reserva

1. Administración configura especialidades, médicos, sedes, consultorios, horarios y bloqueos.
2. El paciente elige especialidad, médico, sede y fecha.
3. La API calcula espacios a partir de disponibilidad, ausencias y citas activas.
4. Al seleccionar un espacio, la API valida de nuevo dentro de una transacción y crea la cita.
5. Se notifica a paciente y médico; la cita se atiende, cancela, reprograma o marca como inasistencia.
6. Al concluir la atención, se registra una consulta ligada a la cita y su estado pasa a `completed`.

## Reglas de integridad

- Usar UUID y `TIMESTAMPTZ` en PostgreSQL.
- No permitir traslapes para un médico, consultorio o paciente cuando las citas estén activas.
- Verificar que el médico atienda la especialidad y sede seleccionadas.
- Mantener citas como historial: cancelar o reprogramar en lugar de eliminarlas.
- Permitir una sola consulta por cita y únicamente si la cita está completada.
- Guardar en la cita un motivo breve; tratar notas clínicas como información restringida.

## Estados

`pending`, `confirmed`, `cancelled`, `completed`, `no_show` y `rescheduled`.

Para el MVP, las reservas válidas pueden confirmarse automáticamente. `pending` queda disponible cuando la clínica requiera aprobación manual.
