# SLO de la agenda de citas médicas

Documento de diseño de P02 y Fase 2. Los valores siguientes son objetivos internos del equipo. Ver [reporte y Tabla 2](../practicas/P02/README.md) y [cálculos](../evidencias/P02/calculos.md).

## Servicio y medición común

Servicio: `agenda-medica`. Operaciones previstas: `GET /api/horarios`, `POST /api/citas`, `DELETE /api/citas/{id}` y consulta/actualización de agenda por personal autorizado. Son contratos propuestos de medición; aquí no se implementa una API.

Una reserva termina bien únicamente después del commit de SQL, con una cita única por médico y horario. Cita y trabajo de comprobante se guardan en una misma transacción mediante una tabla outbox. La respuesta incluye el identificador de cita; no espera a Functions ni a Blob. Un conflicto legítimo devuelve 409 y no crea otra cita. Los reintentos con la misma clave de idempotencia devuelven la reserva existente.

Punto principal: proxy HTTP de la VM, antes de la API, con registros JSON locales. En alta disponibilidad se suman los registros de ambos proxies sin duplicar eventos. Campos del contrato de registro: `timestamp_utc`, `request_id` único por intento HTTP, `operation`, `origin` (`user` o `synthetic`), `valid`, `status`, `duration_ms`, `outcome` y `persisted`. No se registran nombres de pacientes, credenciales ni información clínica.

Eventos válidos: intentos de usuarios sobre las operaciones indicadas, autenticados y con entradas correctas. Se excluyen sondeos, bots identificados y errores de cliente comprobados (400 por formato, 401/403 por credenciales, 404 por recurso inexistente, 409 por horario ya ocupado, 422 por validación). No se excluyen todos los 4xx indiscriminadamente: 429 por falta de capacidad, 5xx, 502/504 y timeouts son malos si la petición era válida. Si la API no responde, el proxy aplica el timeout de 5 s y registra el fallo; un evento sin clasificación suficiente se conserva conservadoramente como válido y malo para no ocultar fallas.

Herramientas gratuitas previstas: logs JSON + un agregador Python local ejecutado cada 5 minutos mediante cron; archivo de resultados y revisión por el responsable. Retención mínima 35 días en disco, con rotación. No se requiere ingestión pagada en Azure Monitor; Azure Monitor/Service Health se usa para corroborar fallas del proveedor. El disco y la VM ya están presupuestados. La instrumentación y el agregador se implementarán en la fase de desarrollo, no se presentan como ejecutados en P02.

Verificación externa: UptimeRobot gratuito, intervalo de 5 minutos, sobre `GET /health/ready` del mismo endpoint público. Responde 200 únicamente si API y una consulta de SQL funcionan; devuelve 503 si no. No comprueba una escritura ni sustituye el SLI de reservas. La URL será el hostname del despliegue; no se inventa una URL pública antes de desplegar. Se guardará captura y exportación mensual del monitor cuando exista. Configurar TLS, timeout y notificaciones disponibles en el plan gratuito; corroborar un sondeo fallido antes de atribuirlo al servicio.

Si el proxy completo está caído, sus logs no ven los intentos que no llegaron. Por eso el monitor externo tiene un registro temporal separado: no se mezcla su denominador con el de solicitudes reales. Una falla externa abre incidente y bloquea despliegues de riesgo aunque no haya peticiones registradas. Si faltan logs o la ventana tiene cero eventos, el SLI es **sin datos**, nunca 100 %. Se reporta cobertura de telemetría; un hueco impide afirmar cumplimiento.

## SLO 1 Disponibilidad de la agenda

- **SLI definición:** proporción de solicitudes válidas completadas correctamente.
- **Evento bueno:** respuesta 2xx con `outcome=success`; para reservar, `persisted=true` tras el commit y sin duplicidad; para cancelar, cancelación persistida o repetición idempotente correctamente resuelta. Un 200 con resultado incorrecto no es bueno.
- **Implementación:** deduplicar por `request_id`; `100 × count(valid AND good) / count(valid)`. La deduplicación evita contar dos veces el mismo log; los reintentos HTTP distintos sí son intentos distintos.
- **Ventana:** últimos 30 días móviles en UTC, recalculados cada 5 minutos.
- **Objetivo:** ≥99.5 %.
- **Justificación:** el modelo base de agenda da 99.890010 %; la meta reserva margen para errores de código, operación y cambios. No se acredita disponibilidad medida.
- **Presupuesto operativo:** `0.005 × N` solicitudes malas admitidas, donde N es el total válido de la ventana.
- **Equivalente temporal para P02:** `0.005 × 43200 = 216 min`. No representa minutos de caída medidos por el SLI de eventos.
- **Alertas:** consumo `errores/(0.005 × N)`; aviso al llegar al 50 % (equivalente 108 min), crítica al 100 % (216 min). Con N=100000: presupuesto 500 errores, aviso 250 y crítica 500.
- **Política:** política común descrita abajo; también aplica a indisponibilidad detectada externamente.
- **Responsable propuesto:** Gustavo Linares Villegas; suplente operativo Alumno 2.
- **Revisión:** semanal y al cierre de cada parcial.

## SLO 2 Latencia de consulta y reserva

- **SLI definición:** solicitudes válidas de `GET /api/horarios` y `POST /api/citas` que terminan correctamente en menos de 1000 ms, entre todas las solicitudes válidas de esas operaciones.
- **Evento bueno:** éxito según SLO 1 y `duration_ms < 1000`, medido desde recepción en el proxy hasta envío de la respuesta. Los fallos y timeouts cuentan como malos, aunque respondan rápido. Se excluyen los conflictos 409 legítimos bajo el mismo criterio de eventos válidos.
- **Implementación:** `100 × count(valid AND good AND duration_ms < 1000) / count(valid)` con filtro de las dos operaciones. Se calcula también por operación para evitar que las consultas oculten lentitud al reservar.
- **Ventana:** 30 días móviles, UTC, actualización cada 5 minutos.
- **Objetivo:** ≥95 % de eventos buenos rápidos; p95 de duración se reporta como diagnóstico complementario. La proporción es la definición usada para presupuestar.
- **Justificación:** meta inicial de interacción de agenda, no valor prometido por Microsoft ni resultado de una prueba. Debe validarse posteriormente con carga representativa; cualquier cambio queda versionado, nunca se ajusta retroactivamente para ocultar incumplimientos.
- **Presupuesto operativo:** `0.05 × N` eventos malos o lentos permitidos en las operaciones incluidas.
- **Equivalente temporal para P02:** `0.05 × 43200 = 2160 min`; no se interpreta como tiempo literal tolerado de respuesta ni caída real.
- **Alertas:** aviso al consumir 50 % (1080 min equivalentes), crítica al 100 % (2160 min equivalentes). Con N=100000: presupuesto 5000 eventos, aviso 2500 y crítica 5000.
- **Herramienta/punto:** logs y agregador del proxy; monitor externo complementario de disponibilidad. El sondeo gratuito no acredita latencia de una reserva real.
- **Política:** política común; un fallo lento consume ambos presupuestos cuando pertenece a ambos denominadores.
- **Responsable propuesto:** Alumno 3; Gustavo decide el levantamiento del congelamiento.
- **Revisión:** semanal y al cierre de cada parcial.

## Política común del presupuesto

El mantenimiento propio cuenta como fallo en los SLO internos cuando afecta solicitudes válidas. Las exclusiones limitadas del SLA externo no se trasladan automáticamente al presupuesto interno. Se conserva la cobertura de logs durante cambios planificados.

1. Por debajo del 50 %: cambios normales con revisión.
2. Desde el 50 %: responsable abre revisión de incidentes y verifica telemetría.
3. Desde el 80 %: se posponen nuevas funciones no esenciales y cambios de alto riesgo; se permiten correcciones pequeñas revisadas.
4. Desde el 100 % en cualquiera de los SLO: se congelan nuevas funciones; únicamente cambios de recuperación, confiabilidad o seguridad.
5. Recuperación: reanudar cuando **ambos** SLO tengan al menos el 25 % de su presupuesto disponible (consumo ≤75 %), no haya incidente externo abierto ni huecos de telemetría, y exista causa/acción documentada. Decide Gustavo Linares Villegas con revisión de otro integrante.

En una ventana móvil se recupera presupuesto cuando salen eventos malos antiguos o cambia la proporción al entrar eventos válidos nuevos. No se borran errores ni se reinicia arbitrariamente la ventana.

## Casos de comprobación de la especificación

| Caso | Disponibilidad | Latencia | Comportamiento requerido |
|---|---|---|---|
| Reserva persistida sin duplicidad en 600 ms | Bueno | Bueno | 201 e identificador de cita |
| Reserva persistida en 1500 ms | Bueno | Malo | No perder reserva; investigar lentitud |
| Dos usuarios reservan el mismo horario | Ganador bueno; conflicto 409 excluido | Ganador según duración; conflicto excluido | Restricción única transaccional; solo una cita |
| SQL falla y la API responde 503 | Malo | Malo en consulta/reserva | No confirmar una cita no guardada |
| SQL confirmó pero se perdió la respuesta | Intento malo para el usuario | Malo | Reintento idempotente recupera la misma cita |
| Timeout a los 5 segundos | Malo | Malo | Registrar 504; no asumir que SQL hizo rollback |
| Function o Blob falla después de confirmar | No cambia éxito de reserva | No cambia duración de reserva | Outbox conserva trabajo, reintentar; comprobante pendiente |
| API caída y sin logs de usuario | Sin datos en ese tramo; incidente externo | Sin datos | Monitor detecta; no afirmar 100 % |
| 100000 eventos válidos y 500 fallos | 99.5 %; presupuesto agotado | Depende de lentos adicionales | Alerta crítica y congelamiento |

Estas son comprobaciones documentales, no resultados de ejecución de una aplicación existente.
