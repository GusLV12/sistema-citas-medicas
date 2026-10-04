# Práctica 2 · SLA y SLO de la agenda de citas médicas

**Sistemas Distribuidos · 7CV1 · ESCOM · Semestre 27/1**

Integrantes: Gustavo Linares Villegas, Alumno 2 y Alumno 3. Los dos últimos identificadores se sustituirán por sus nombres reales.
Actualización: 04/10/2026.

## 1. Proyecto, alcance y fuentes

El sistema permite consultar horarios, reservar y cancelar citas y administrar la agenda del consultorio. La aplicación y API viven en Azure Virtual Machines; Azure SQL Database conserva horarios y reservas; Azure Functions Flex genera comprobantes; Azure Blob Storage los almacena. Azure DNS resuelve el dominio y, en el escenario redundante, Azure Load Balancer Standard distribuye el tráfico entre dos VM. Estos dos últimos son dependencias auxiliares incluidas en cálculos y costos.

La reserva queda confirmada al persistir en SQL, junto con un trabajo pendiente en una tabla outbox. La generación del comprobante es posterior: su fallo no convierte una reserva confirmada en fallida. No se incluyen expedientes clínicos, diagnóstico, pagos, correo ni Kubernetes. App Service y Container Apps no forman parte de esta propuesta.

El [diagrama definitivo y sus flujos](../../docs/arquitectura/arquitectura-p02.md) distingue reserva síncrona y comprobante asíncrono.

Las condiciones contractuales se obtuvieron de los documentos oficiales de Microsoft, edición **01/09/2026**, revisada el **03–04/10/2026**. Fuentes: [catálogo oficial de SLA](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), [contrato inglés](https://www.microsoft.com/licensing/docs/documents/download/OnlineSvcsConsolidatedSLA%28WW%29%28English%29%28September_2026%29%28CR%29.docx) y [evidencias](../../evidencias/P02/README.md).

### Tabla 1. Anatomía de los SLA

En todas las filas, **P**, **E** y **R** remiten a las condiciones comunes inmediatamente después de la tabla; forman parte de cada análisis. Los créditos se aplican al cargo elegible del recurso afectado, no a toda la solución. Los fragmentos entre comillas se transcriben del contrato inglés aportado; las definiciones completas están en [extractos contractuales](../../evidencias/P02/fuentes/extractos-sla.md).

| Responsable propuesto | Servicio, fuente y fecha | Compromiso por configuración | Definición literal y medición | Exclusiones | Créditos | Reclamación y remedio | Minutos equivalentes / 30 d; crédito con 99.0 % sobre USD 100 |
|---|---|---|---|---|---|---|---|
| Gustavo Linares Villegas | Virtual Machines; [SLA oficial](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), sección Virtual Machines, 01/09/2026; revisión 04/10/2026 | Individual: todos los discos SO Premium SSD y datos Premium SSD/Premium SSD v2/Ultra: **99.9 %**; Standard SSD **99.5 %**; HDD **95 %**. Dos o más VM en Availability Set: **99.95 %**; en dos o más zonas: **99.99 %** | Individual: “Downtime: is the total accumulated minutes that are part of Minutes in the Applicable Period that have no Virtual Machine Connectivity.” Minutos sin conectividad TCP/UDP permitida; en conjuntos/zonas debe faltar conectividad del conjunto según la cláusula. P | E1–E6; configuración/discos exigidos; con discos de varios tipos aplica el SLA menor; shared disks no reciben automáticamente SLA de Availability Set | Premium/set/zonas: <objetivo: 10 %; <99 %: 25 %; <95 %: 100 %. SSD Standard: <99.5: 10 %, <95: 25 %, <90: 100 %. HDD: <95: 10 %, <92: 25 %, <90: 100 % | R; sí, crédito como remedio único | Premium **43.2; USD 10**. SSD **216; USD 10**. HDD **2160; USD 0**. Set **21.6; USD 10**. Zonas **4.32; USD 10** |
| Alumno 2 | SQL Database; [SLA oficial](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), sección Azure SQL Database, 01/09/2026; revisión 04/10/2026 | GP/Business Critical/Premium/Hyperscale sin redundancia de zona: **99.99 %**; con redundancia de zona: **99.995 %**. Basic/Standard: **99.99 %**, no son la opción zonal elegida | “A minute is considered unavailable for a given Database if all continuous attempts by Customer to establish a connection to the Database within the minute fail.” Unidad: minuto; minutos desplegados en P | E1–E6; fallos de consultas/código del cliente no equivalen a imposibilidad de conectar; operaciones iniciadas por cliente y mantenimiento excluidos según contrato | <objetivo: 10 %; <99 %: 25 %; <95 %: 100 % | R; sí | Sin zonas/Basic/Standard **4.32; USD 10**. Con zonas **2.16; USD 10** |
| Alumno 3 | Blob Storage; [SLA oficial](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), sección Storage Accounts, 01/09/2026; revisión 04/10/2026 | Hot LRS/ZRS/GRS/GZRS: lectura/escritura **99.9 %**. Hot RA-GRS/RA-GZRS: lectura **99.99 %**, escritura **99.9 %**. Se elige Hot LRS → Hot ZRS | “Uptime Percentage: Uptime Percentage is calculated using the following formula: 100% − Average Error Rate”. Promedio de tasas horarias de transacciones fallidas en P; hora sin transacciones: tasa 0 %. No es un contador de minutos de caída. Put/GetBlob: procesamiento máximo 2 s × MB transferidos | E1–E6; autenticación, cuotas, timeout del cliente demasiado corto, falta de backoff; en lectura RA se exige intentar secundaria y se excluye retraso de georreplicación | Escritura y lectura ordinaria: <99.9: 10 %, <99: 25 %. Lectura RA: <99.99: 10 %, <99: 25 %. No hay escalón 100 % en esta cláusula | R; sí | Ordinario/escritura RA **43.2; USD 10**. Lectura RA **4.32; USD 10**. Son equivalentes pedagógicos, no la unidad contractual |
| Gustavo Linares Villegas, análisis complementario | Functions; [SLA oficial](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), sección Azure Functions, 01/09/2026; revisión 04/10/2026 | **99.95 %** en Consumption, Flex Consumption, Premium y Dedicated; se elige **Flex Consumption** de pago por uso | Flex/Premium/Dedicated: “A minute is considered unavailable for a given Function App when there is no connectivity between plan on which the Function App is hosted (the Flex Consumption plan, Premium plan, or the Dedicated App Service plan) and Microsoft’s Internet gateway.” Minutos en P. Consumption: ejecución sin salida en log 5 min después de disparo correcto | E1–E6; fallo del código o del trigger configurado por cliente no basta para acreditar caída de plataforma; no confundir consumo clásico con Flex | <99.95: 10 %; <99: 25 %; <95: 100 % | R; sí | Todos los planes analizados: **21.6; USD 10**; para Consumption los minutos son solo equivalentes |

**P · Periodo.** Para servicios medidos Pay As You Go, el contrato define Applicable Period como los 30 días anteriores e incluido el primer día del incidente reclamado; para otros servicios usa el mes calendario. Se aplica aquí la primera definición, no se sustituye por el mes de factura. Los cálculos comparativos normalizan 30 días = 43 200 min. El período de costos de calculadora es, en cambio, 730 h. VM, SQL y Flex usan minutos; Storage usa tasas horarias y Consumption clásico ejecuciones. Multiplicarlos sirve como modelo académico, no crea un SLA contractual extremo a extremo.

**E · Exclusiones comunes para cada servicio.** E1: factores fuera del control razonable del proveedor, incluida red externa. E2: hardware, software o servicios de terceros. E3: configuración no admitida, uso contrario a indicaciones o falta de medidas de seguridad del cliente. E4: entradas inválidas, cuotas excedidas o throttling por abuso. E5: previews, pruebas, niveles gratuitos y compras mediante créditos de suscripción según las condiciones generales. E6: operaciones iniciadas por el cliente, mantenimiento excluido y degradación de latencia sin indisponibilidad contractual. La cláusula también excluye dependencia de un único centro de datos sin resiliencia geográfica en las condiciones descritas; no debe interpretarse el porcentaje aislado de sus exclusiones. El mantenimiento programado general requiere aviso de al menos cinco días.

**R · Reclamación.** Microsoft debe recibir la reclamación de Azure dentro de **60 días del incidente**, por soporte, con descripción, fechas/horas y duración, nombres de recursos, número y ubicación de usuarios afectados y errores. La evaluación suele tomar 45 días, sin que ello garantice aprobación. Los créditos son el **remedio único y exclusivo**, se limitan a cargos elegibles del servicio/recurso afectado y no cubren ingresos perdidos. Un comunicado de incidente no prueba elegibilidad. Los escalones son estrictos: **99.0 % no es menor que 99 %**; por eso en los cuatro servicios corresponde 10 %, salvo VM HDD que no incumple su 95 %.

**México.** Las cláusulas de estos cuatro servicios no fijan un porcentaje especial para Querétaro/México. Esto no garantiza que cualquier SKU o redundancia esté disponible allí. La arquitectura presupuestada está en East US. La pregunta 3 analiza por separado la residencia mexicana.

**Control de traducción.** El texto inglés incluye General Purpose en la cláusula SQL sin zonas de 99.99 %; la versión española proporcionada omite ese nombre en ese párrafo. Se usa el texto inglés identificado, sin ocultar la discrepancia ni atribuir la misma redacción a ambas versiones.

**Dependencias auxiliares.** Azure DNS: 100 %, 0 min equivalentes, crédito a 99.0 % de USD 100 = USD 100; escalones <100: 10 %, <99.99: 25 %, <99.5: 100 %. Exige consultas válidas a todos los servidores, respuestas dentro de 2 s y reintentos continuos de al menos 60 s. Load Balancer Standard: 99.99 %, 4.32 min equivalentes, crédito a 99.0 % = USD 25; escalones <99.99: 10 %, <99.9: 25 %. Su denominador exige servir dos o más VM saludables; indisponibilidad cuando todas carecen de conectividad por el endpoint en un minuto; agotamiento SNAT excluido y Basic sin SLA. Se aplican P, E y R. Fuente, versión y revisión: el mismo contrato, secciones Azure DNS y Azure Load Balancer. Un compromiso del 100 % significa un umbral para créditos, no imposibilidad física de fallo.

## 2. Dependencias, disponibilidad y costo

Véanse el [diagrama](../../docs/arquitectura/arquitectura-p02.md), el [presupuesto detallado](costos.md) y los [cálculos reproducibles](../../evidencias/P02/calculos.md). Región East US; USD; mismos supuestos de carga en ambos escenarios; recursos de pago sin descuentos por reserva ni créditos promocionales.

### Tabla 2. Disponibilidad compuesta

| Componente | SLA base | SLA redundante | Serie o paralelo | Costo extra USD/mes |
|---|---:|---:|---|---:|
| Azure DNS | 100 % | 100 % | Dependencia de resolución de agenda | 0.00000 |
| Load Balancer Standard | No instalado | 99.99 % | En serie con la capa VM, solo redundante | 18.30000 |
| VM B2s Linux con discos Premium | 99.9 % | 99.99 % publicado para dos VM entre zonas | Una VM → dos VM en paralelo; capa en serie con SQL | 35.64750, incluida VM adicional y disco |
| IP Standard | Incluida en conectividad | Incluida en conectividad | Una → tres IP; no se inventa SLA separado | 7.30000 |
| SQL GP Gen5 2 vCore | 99.99 % | 99.995 % zonal | En serie con API; también usado por outbox | 138.12580 |
| Functions Flex | 99.95 % | 99.95 % | Solo comprobante, sin mejora contractual supuesta | 0.00000 |
| Storage Hot (host y comprobantes) | 99.9 % LRS | 99.9 % ZRS | Solo flujo asíncrono; almacenamiento agrupado | 0.16650 |
| **Compuesto agenda** | **99.890010 %** | **99.975002 %** | DNS × [LB] × capa VM × SQL | **199.53980 total** |
| **Minutos equivalentes agenda / 30 d** | **47.51568** | **10.79914** | Ventana de 43 200 min | — |
| Compuesto generación de comprobante | 99.840065 % | 99.8450575 % | SQL × Functions × Storage | Incluido arriba |
| Minutos equivalentes comprobante / 30 d | 69.09192 | 66.93516 | No es plazo de entrega del comprobante | — |
| **Costo total USD / 730 h** | **416.13** | **615.67** | Estimaciones académicas | **199.54** |

Para componentes en serie, `A = a1 × a2 × …`; minutos equivalentes `M = (1 − A) × 43200`.

```text
Agenda base:       1 × 0.999 × 0.9999 = 0.9989001
Agenda redundante: 1 × 0.9999 (LB) × 0.9999 (VM entre zonas) × 0.99995 (SQL)
                   = 0.9997500199995
Comprobante base:  0.9999 × 0.9995 × 0.999 = 0.99840064995
Comprobante red.:  0.99995 × 0.9995 × 0.999 = 0.998450574975
```

La fórmula ideal para dos componentes independientes en paralelo es `1 − (1 − a1)(1 − a2)`: dos VM de 99.9 % darían 99.9999 %. No se usa ese resultado como garantía: las fallas de región, red y configuración pueden ser comunes. La tabla usa **99.99 % publicado para la configuración de VM entre zonas**. Tampoco el producto de SLA con definiciones diferentes prueba independencia, disponibilidad observada ni obligación contractual conjunta. Es la aproximación exigida por la práctica; la medición del usuario se define aparte.

La VM individual es el eslabón débil de la agenda base. Reforzar únicamente esa capa, con balanceador, VM, disco e IP adicionales, cuesta **USD 61.2475/mes** y eleva el modelo a **99.970003 %** (12.95870 min). En el diseño redundante VM y LB, ambos 99.99 %, limitan más que SQL. En comprobantes, Storage Hot 99.9 % domina; cambiar LRS por ZRS mejora tolerancia a fallas de zona, pero **no aumenta el porcentaje contractual Hot**. Functions permanece en 99.95 %.

## 3. SLO y SLA del equipo

### Tabla 3. SLO del proyecto

El [documento central `docs/slo.md`](../../docs/slo.md), enlazado desde [Fase 2](../../docs/fase2.md), contiene definiciones implementables, casos y responsables. Los conflictos legítimos 409 y errores comprobados de cliente se excluyen; 5xx, 429 por capacidad, resultados incorrectos y timeouts de peticiones válidas son malos. El mantenimiento del equipo consume el SLO interno.

| SLO | SLI: buenos / válidos | Punto de medición | Ventana | Objetivo | Presupuesto equivalente | Alertas 50 % / 100 % | Herramienta y responsable propuesto |
|---|---|---|---|---|---|---|---|
| Disponibilidad de agenda | Solicitudes válidas con respuesta correcta / todas las válidas de horarios, reservas, cancelación y agenda. Reserva buena exige commit sin duplicidad | Proxy/API de cada VM; logs deduplicados por intento | 30 días móviles UTC | ≥99.5 % | 216 min; operativo: 0.005 × N errores | 108 / 216 min; operativo: 0.0025 × N / 0.005 × N errores | Logs JSON + agregador Python propuesto; UptimeRobot externo cada 5 min; Gustavo, suplente Alumno 2 |
| Latencia de consulta/reserva | Solicitudes válidas correctas en <1000 ms / todas las válidas GET horarios y POST citas; fallos también son malos | Duración desde recepción hasta respuesta en proxy | 30 días móviles UTC | ≥95 %; p95 diagnóstico | 2160 min; operativo: 0.05 × N malos/lentos | 1080 / 2160 min; operativo: 0.025 × N / 0.05 × N | Mismos logs/agregador, separado por operación; Alumno 3 |

El 99.5 % deja margen frente al 99.890010 % calculado para la agenda base; ello apoya una meta inicial, no acredita que el código la alcance. La latencia es una meta de diseño sin prueba de carga. Los minutos de latencia son una conversión académica, no minutos literales de indisponibilidad. Con 100 000 solicitudes, disponibilidad permite 500 fallos y latencia 5000 eventos malos/lentos. Cero eventos o falta de logs significa **sin datos**, nunca 100 %.

Al 50 % se revisan incidentes; al 80 % se posponen funciones no esenciales; al 100 % de cualquiera de los presupuestos se congelan funciones nuevas. Se permiten reparaciones y seguridad. Gustavo y otro revisor autorizan reanudar cuando ambos recuperen al menos 25 % disponible, haya revisión de causa y no existan incidentes ni huecos de telemetría. Los sondeos externos no se mezclan con el denominador de solicitudes; detectan caídas completas invisibles al proxy. UptimeRobot Free ofrece intervalo de cinco minutos para este uso académico; la instrumentación sigue siendo un plan, no una medición realizada. [Fuente del monitor, consulta 04/10/2026](https://uptimerobot.com/pricing/).

### Cláusula propuesta de SLA externo

Ofreceríamos **99.0 % de disponibilidad mensual** de consulta, reserva y cancelación de citas. Se mide por mes calendario UTC como `100 × solicitudes válidas correctas / solicitudes válidas elegibles`, según las reglas de `docs/slo.md`: una reserva solo es correcta tras persistirse sin duplicar horario. Respuestas 5xx, timeouts, saturación imputable al servicio y resultados incorrectos cuentan como fallos; la falta de comprobante posterior no invalida la reserva. Un intervalo sin telemetría se investiga con evidencia del cliente y del monitor y no acredita cumplimiento por ausencia de datos.

Se excluyen únicamente solicitudes dentro de mantenimiento anunciado con 48 h de anticipación, domingos 02:00–02:30, zona America/Mexico_City; entradas o credenciales inválidas comprobadas; problemas de red/equipo exclusivos del cliente; y fuerza mayor documentada fuera del control razonable del equipo. Solo se excluye el tramo efectivamente afectado, sin extenderlo al mes. Los fallos ordinarios de Azure y los despliegues defectuosos del equipo no quedan automáticamente excluidos de nuestra promesa. El mantenimiento sí consume el presupuesto interno, aunque pueda excluirse del SLA externo.

Si el indicador mensual resulta de 95.0 % a menos de 99.0 %, el crédito será 10 %; de 90.0 % a menos de 95.0 %, 25 %; por debajo de 90.0 %, 100 % de la cuota mensual del servicio de agenda afectado. Se aplica un único escalón, sin superar esa cuota. La reclamación se presenta al responsable del servicio mediante ticket, dentro de 30 días naturales después del cierre del mes, con cuenta afectada, fechas UTC, operación, identificadores de solicitud y evidencia disponible. El equipo responderá en 15 días hábiles y aplicará el crédito a la siguiente factura; un servicio sin cuota no genera crédito monetario. Es una cláusula académica propuesta, no un contrato celebrado. El SLO interno de 99.5 % es más exigente para permitir corregir degradaciones antes de incumplir el compromiso externo de 99.0 %.

## 4. Respuestas de análisis

### 1. Falla de aplicación que no cuenta para Azure

Una versión defectuosa puede rechazar todas las reservas con 500 aunque la VM conserve conectividad y SQL acepte conexiones. No cumple las definiciones contractuales de caída de VM o SQL: cae del lado del equipo en responsabilidad compartida. Nuestro SLI de disponibilidad registra esos intentos válidos como malos; el de latencia de consulta/reserva también, aunque respondan en 50 ms. Por ejemplo, 250 errores sobre 100 000 intentos consumen 50 % del presupuesto de disponibilidad de 500. Un 200 con reserva no persistida tampoco es éxito.

### 2. Ocho horas de caída y pérdida de negocio

Supóngase una caída elegible de conectividad de la VM individual durante 480 min de una ventana comparativa de 43 200 min: `A = 98.888889 %`, escalón **25 %**. Usando como aproximación de cargos elegibles la VM de la estimación, el crédito sería `0.25 × USD 30.368 = USD 7.592`, aproximadamente **USD 7.59**, no 25 % de los USD 416.13 de toda la solución. La liquidación real depende del Applicable Period contractual y de los cargos efectivamente pagados: 730 h de calculadora no son 720 h del ejemplo. Como escenario de negocio, se suponen 4 reservas por hora, USD 25 de ingreso por consulta y 50 % de reservas no recuperadas: `8 × 4 × 25 × 0.5 = USD 400` de ingreso potencial perdido, no utilidad neta ni consumo observado. El crédito cubriría alrededor de 1.90 % de esa pérdida. Si la caída fuera un bug propio, el crédito Azure sería cero. No se aportó una estimación P1 identificable; se usa la estimación académica documentada en [costos](costos.md), sin atribuirle origen en P1.

### 3. Google México, 99.99 % y residencia de datos

El [SLA de Compute Engine](https://cloud.google.com/compute/sla), versión 04/03/2025 citada por la práctica y consultada en la revisión inicial del 03/10/2026, asigna a multizona y balanceo Premium Tier en México **99.95 %**, frente a 99.99 % de otras regiones indicadas. Dos zonas dentro de Querétaro no convierten ese contrato en 99.99 %: cómputo × balanceador ya da `0.9995² = 99.900025 %`, antes de base de datos. Una arquitectura candidata sería dos instalaciones completas en sitios mexicanos con dominios de falla independientes, ingreso redundante y datos, copias, logs y respaldos exclusivamente en México; la base debe usar consenso y control de escritor para evitar reservas duplicadas, con quórum distribuido en al menos tres dominios y conmutación probada. Como hipótesis, dos rutas completas de 99.95 % independientes producirían `1 − 0.0005² = 99.999975 %`; dejando 99.995 % al plano común de datos/enrutamiento resultaría **99.994975 %**. Son supuestos de ingeniería, no SLA de Google ni porcentajes ya demostrados. El [presupuesto exploratorio](costos.md#alternativa-de-residencia-en-méxico-pregunta-3) suma **USD 1300/mes**, con asignaciones académicas explícitas, no una cotización verificada. La respuesta honesta es que esa arquitectura puede perseguir la meta, pero los documentos disponibles no permiten garantizarla ni cerrar un precio real; se requieren cotizaciones locales, verificación de residencia y pruebas de fallas antes de ofrecer 99.99 %.

### 4. Dos mejoras y costo

Dentro del modelo de la Tabla 2, prometer más disponibilidad de la que admiten las dependencias dejaría sin margen al código, despliegues y operación; además, el producto no sustituye una medición real. La primera mejora es duplicar VM en zonas distintas, con disco, red y balanceador: **USD 61.2475 adicionales/mes**, compuesto **99.970003 %** y 12.95870 min equivalentes. La segunda es habilitar redundancia zonal en SQL GP: **USD 138.1258 adicionales/mes**; aplicada sola al escenario base, **99.895005 %**, 45.35784 min. Juntas producen **99.975002 %**, 10.79914 min; el costo combinado aumenta USD 199.3733, y al añadir USD 0.1665 de Storage ZRS se llega al incremento total **USD 199.5398**. La mejora con mayor efecto inicial es la capa VM, no SQL ni los comprobantes.

### 5. Incidente oficial de 2025

El [PIR de Azure Front Door YKYN-BWZ](https://azure.status.microsoft/en-us/status/history/?trackingId=YKYN-BWZ), revisado el 04/10/2026, describe afectación del 29/10/2025 15:41 UTC al 30/10/2025 00:05 UTC: **504 min**, con recuperación parcial antes del final. Un defecto de procesamiento de configuraciones provocó errores de conexión y DNS; el impacto varió por cliente. Son fallas de plataforma potencialmente reclamables, pero el informe no demuestra créditos concedidos: hay que acreditar recurso, contrato vigente en el incidente y métricas exigidas. Nuestra arquitectura no usa Front Door; que SQL aparezca entre servicios afectados tampoco demuestra caída de nuestras consultas. Por ello no afirmamos afectación ni crédito real. Si la agenda hubiera fallado durante los 504 min completos, el monitor externo de disponibilidad detectaría la pérdida de acceso en el siguiente sondeo, hasta unos cinco minutos después; con tráfico, los errores o la latencia podrían avisar antes. El consumo temporal equivalente sería `504/216 = 233.33 %`, exceso de **288 min**. El presupuesto real por solicitudes depende del tráfico fallido y no puede deducirse solo del PIR; en este proyecto sin despliegue no se ha observado consumo.

### 6. 80 % del presupuesto en la primera semana

Se pospone la función nueva del viernes conforme a la política de `docs/slo.md`; solo se consideran cambios pequeños de recuperación o seguridad revisados. El 80 % del presupuesto de disponibilidad equivale a **172.8 min** de los 216, con **43.2 min** equivalentes restantes; para 100 000 solicitudes serían 400 fallos de los 500 permitidos. Se revisan causa, logs, cobertura y carga antes de autorizar nuevos riesgos. La ventana es móvil de 30 días, no se reinicia por comenzar otra semana o mes. Gustavo, con un revisor, autoriza reanudar cuando ambos presupuestos tengan al menos 25 % disponible y se cumplan las condiciones de recuperación.

## 5. Evidencias y contribuciones

El [índice de evidencias](../../evidencias/P02/README.md) enlaza contratos, capturas, calculadora y cálculos. La [bitácora](../../bitacora/2026-09-15.md) registra las decisiones del proyecto.

| Integrante | Responsabilidad | Revisión cruzada |
|---|---|---|
| Gustavo Linares Villegas | VM, Functions, contratos y evidencias | Costos y disponibilidad compuesta |
| Alumno 2 | SQL Database, arquitectura, costos y Tabla 2 | Presupuestos y Tabla 3 |
| Alumno 3 | Blob Storage, SLO, SLA y respuestas | Contratos y Tabla 1 |

Cada integrante actualizará su nombre, registrará su aportación y realizará su commit correspondiente.

### Lista de verificación

- [x] Cuatro servicios con función definida y categorías de cómputo, base gestionada y objetos.
- [x] Tabla 1: configuración, definición, periodo, exclusiones, créditos, reclamación, fuentes y minutos.
- [x] Tabla 2 y diagrama con flujos separados, costos y fórmulas reproducibles.
- [x] Tabla 3 y dos SLO completos enlazados desde Fase 2; SLA externo menos exigente.
- [x] Seis respuestas con cifras y supuestos diferenciados de hechos.
- [x] Bitácora, referencias, declaración de IA y reparto de responsabilidades.
- [ ] Contrastar estimación con la P1 real si el docente exige continuidad exacta: ese archivo no está disponible.
- [ ] Sustituir Alumno 2/3, registrar aportaciones y completar revisión cruzada.
- [ ] Capturas personales con usuario real y encabezado/fecha de la página oficial, si se exige ese formato literal: las guardadas son páginas renderizadas del contrato oficial.
- [ ] Cerrar cotización real y validación de disponibilidad/residencia de la alternativa México antes de presentarla como solución garantizada; el cálculo actual es exploratorio.
- [ ] Al final: integrar en GitHub y hacer un commit real por integrante, con el análisis que haya revisado y aportado.

Word, OpenSLO y monitoreo real de 24 h no forman parte de esta entrega.

## 6. Conclusiones

La confirmación de una cita depende de VM y SQL; separar comprobantes evita que una falla de Functions o Blob invalide una reserva persistida. El modelo de agenda pasa de 99.890010 % a 99.975002 % con redundancia y aumenta el presupuesto de USD 416.13 a USD 615.67 al mes. La primera inversión útil es reforzar la VM individual. El SLO 99.5 % y el SLA propuesto 99.0 % dejan margen frente al modelo, pero deben validarse cuando exista la aplicación. Los créditos del proveedor compensan una fracción del recurso afectado y no las pérdidas del consultorio.

## 7. Uso de IA

Se utilizó IA generativa como apoyo para organizar el reporte, revisar fórmulas de disponibilidad y preparar borradores de redacción. Las fuentes oficiales, cálculos y decisiones de arquitectura se documentan en las referencias y evidencias del proyecto. Cada integrante es responsable de revisar y explicar su parte antes de la entrega.

## 8. Referencias

1. Consigna de Práctica 2 entregada en el curso, secciones B1–B4, preguntas 1–6 y rúbrica. Revisada 04/10/2026.
2. Microsoft, [SLA for Online Services](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), edición 01/09/2026 aportada; secciones General Terms, VM, SQL Database, Storage Accounts, Functions, DNS y Load Balancer. Extracción/revisión 03–04/10/2026; [extractos](../../evidencias/P02/fuentes/extractos-sla.md).
3. Microsoft, [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices) y [calculadora](https://azure.microsoft.com/en-us/pricing/calculator/). Tarifas/evidencias 03/10/2026; [detalle de costos](costos.md).
4. Microsoft, [Reliability in Azure SQL Database](https://learn.microsoft.com/en-us/azure/reliability/reliability-sql-database), [Azure Functions](https://learn.microsoft.com/en-us/azure/reliability/reliability-functions) y [regiones](https://learn.microsoft.com/en-us/azure/reliability/regions-list). Revisión 04/10/2026.
5. Google Cloud, [Compute Engine SLA](https://cloud.google.com/compute/sla), edición 04/03/2025 referida en la consigna; consulta inicial 03/10/2026. Se usa para contraste contractual de México, no como fuente del presupuesto hipotético.
6. Microsoft, [PIR Azure Front Door, YKYN-BWZ](https://azure.status.microsoft/en-us/status/history/?trackingId=YKYN-BWZ), incidente 29–30/10/2025; consulta 04/10/2026.
7. UptimeRobot, [Planes](https://uptimerobot.com/pricing/), consulta 04/10/2026; plan gratuito para medición académica propuesta.
