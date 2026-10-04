# Cálculos reproducibles de P02

Generado con `python evidencias/P02/recalcular.py`. Tarifas consultadas el 03/10/2026; no son una factura.

## Disponibilidad

| Flujo | Disponibilidad % | Minutos equivalentes / 30 días |
|---|---:|---:|
| agenda_base | 99.89001000 | 47.51568 |
| agenda_vm_az | 99.97000300 | 12.95870 |
| agenda_sql_zr | 99.89500500 | 45.35784 |
| agenda_redundante | 99.97500200 | 10.79914 |
| comprobante_base | 99.84006500 | 69.09192 |
| comprobante_redundante | 99.84505750 | 66.93516 |
| reserva_y_comprobante_base | 99.74022493 | 112.22283 |
| reserva_y_comprobante_redundante | 99.82508948 | 75.56134 |

## Costos en USD por mes de 730 horas

| Concepto | Base | Redundante | Incremento |
|---|---:|---:|---:|
| VM B2s Linux | 30.36800 | 60.73600 | 30.36800 |
| Disco SO Premium SSD P4 LRS 32 GiB | 5.27950 | 10.55900 | 5.27950 |
| SQL GP Gen5 2 vCore con licencia y 32 GB datos + 9.6 GB log | 372.97118 | 511.09698 | 138.12580 |
| Blob GPv2 Hot 20 GB + 50000 escrituras + 100000 lecturas | 0.70600 | 0.87250 | 0.16650 |
| Functions Flex 50000 ejecuciones de 2 GB por 1 s, importe bruto | 2.62000 | 2.62000 | 0.00000 |
| IP pública Standard (1 base; 1 frontend + 2 salida redundante) | 3.65000 | 10.95000 | 7.30000 |
| Load Balancer Standard hasta 5 reglas + 10 GB | 0.00000 | 18.30000 | 18.30000 |
| Azure DNS público 1 zona y 100000 consultas | 0.54000 | 0.54000 | 0.00000 |
| Salida a Internet 10 GB dentro de 100 GB gratuitos | 0.00000 | 0.00000 | 0.00000 |
| Logs locales y monitor gratuito; sin ingestión pagada | 0.00000 | 0.00000 | 0.00000 |
| **Total** | **416.13468** | **615.67448** | **199.53980** |

## Presupuestos y crédito

Disponibilidad: 0.005 × 43200 = 216 min equivalentes. Alertas: 108 / 216.
Latencia: 0.05 × 43200 = 2160 min equivalentes. Alertas: 1080 / 2160.
Estos presupuestos se consumen por eventos, no por cronómetro: errores / (fracción permitida × solicitudes válidas).
Caída hipotética VM de 8 h: disponibilidad 98.88888889%; crédito 25% × 30.368 USD = 7.592 USD.
Incidente AFD, duración global 504 min: 504/216 × 100 = 233.3333% del presupuesto temporal equivalente, solo si la aplicación hubiera fallado durante todo el intervalo.

## Tabla 1: minutos y crédito a exactamente 99.0 %

Umbrales estrictos; se elige el escalón más alto aplicable. Los minutos convierten porcentajes a 30 días y no reemplazan la métrica contractual de Storage o Consumption.

| Configuración | Objetivo % | Minutos equivalentes | Crédito sobre USD 100 |
|---|---:|---:|---:|
| VM Premium | 99.9 | 43.20 | USD 10.00 |
| VM Standard SSD | 99.5 | 216.00 | USD 10.00 |
| VM Standard HDD | 95 | 2160.00 | USD 0.00 |
| VM Availability Set | 99.95 | 21.60 | USD 10.00 |
| VM entre zonas | 99.99 | 4.32 | USD 10.00 |
| SQL sin zonas / Basic / Standard | 99.99 | 4.32 | USD 10.00 |
| SQL con zonas GP / BC / Premium / Hyperscale | 99.995 | 2.16 | USD 10.00 |
| Blob Hot ordinario y escrituras RA | 99.9 | 43.20 | USD 10.00 |
| Blob Hot lecturas RA | 99.99 | 4.32 | USD 10.00 |
| Functions Consumption / Flex / Premium / Dedicated | 99.95 | 21.60 | USD 10.00 |
| DNS | 100 | 0.00 | USD 100.00 |
| Load Balancer Standard | 99.99 | 4.32 | USD 25.00 |

## Escenarios de las preguntas

Ocho horas: ingreso potencial perdido = 8 × 4 reservas/h × USD 25 × 50 % no recuperado = USD 400; USD 7.592 / USD 400 = 1.898 %.
80 % del presupuesto temporal de disponibilidad: 172.8 min consumidos, 43.2 min restantes.
México (supuestos, no garantía): 0.9995² × 100 = 99.900025 %; [1 − (1 − 0.9995)²] × 0.99995 × 100 = 99.99497500125 %.
Presupuesto exploratorio México = 160 + 540 + 100 + 150 + 150 + 200 = USD 1300/mes. No es cotización.
Los flujos reserva_y_comprobante son una comparación de exigir ambos éxitos; no definen el SLO de agenda ni una entrega instantánea del trabajo asíncrono.
