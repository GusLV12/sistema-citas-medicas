# Costos y supuestos de P02

Estimación académica del 03/10/2026, consolidada el 04/10/2026. Región **East US**, moneda **USD**, **730 horas** al mes, pago por uso, Linux, sin impuestos, soporte pagado, reservas ni Azure Hybrid Benefit. No hay factura, despliegue ni consumo observado. La estimación P1 original no está disponible para verificar continuidad; estas cifras son una nueva base explícita para P02.

## Misma carga para comparar

Una agenda pequeña, 32 GB de datos SQL y 9.6 GB de log presupuestados; 20 GB totales de Storage Hot, 50 000 escrituras y 100 000 lecturas al mes; 50 000 ejecuciones Functions de 2 GB durante 1 s; 100 000 consultas DNS y 10 GB de salida a Internet. Los valores son supuestos de volumen, no resultados de medición. Las operaciones de Storage incluyen una provisión para host/temporizador y comprobantes; al desplegar se medirá su consumo efectivo. Un temporizador cada minuto supone aproximadamente 43 800 activaciones en 730 h: deja unas 6200 ejecuciones de margen dentro de las 50 000. La duración de un segundo por ejecución no está validada.

La licencia SQL se incluye, porque la API de precios del cómputo por sí sola no representa todo el costo del servicio. Se presupuestan respaldos de corto plazo dentro de la franquicia de almacenamiento incluida y no se contrata retención larga; un excedente se cotiza aparte. Logs locales de 35 días deben caber en el disco con rotación; si no, el costo debe ajustarse. No se afirma capacidad suficiente bajo cualquier carga.

## Configuraciones de pago y tarifas

| Recurso | Base | Redundante | Fuente guardada / tarifa usada |
|---|---|---|---|
| VM | 1 B2s Linux | 2 B2s Linux, una por zona | [VM](../../evidencias/P02/fuentes/precios_vm.json): USD 0.0416/h por VM, excluir Windows/Spot |
| Disco SO | 1 Premium SSD P4 LRS, 32 GiB | 2 discos iguales independientes | [Storage](../../evidencias/P02/fuentes/precios_storage.json): USD 5.2795/mes por disco; sin disco HDD/Standard adicional que reduzca SLA |
| SQL | GP Gen5, 2 vCore provisionados, sin zonas | Mismos vCore con redundancia de zona | [SQL](../../evidencias/P02/fuentes/precios_sql.json): cómputo 0.304434/h, incremento zonal 0.18266/h, almacenamiento 0.115 → 0.23/GB-mes; licencia USD 145.95036/mes según calculadora |
| Blob + Storage del host | Hot LRS | Hot ZRS | [Storage](../../evidencias/P02/fuentes/precios_storage.json): 0.0208 → 0.026/GB-mes; escritura 0.05 → 0.0625/10 000; lectura 0.004/10 000 |
| Functions | Flex on-demand | Igual | [Functions](../../evidencias/P02/fuentes/precios_functions.json): 0.000026/GB-s y 0.000004/10 ejecuciones; costo bruto sin descontar franquicia |
| IP Standard | 1 pública | 1 frontend redundante + 2 para salida de VM | [IP](../../evidencias/P02/fuentes/precios_ip.json): 0.005/h por IP |
| Load Balancer | No instalado | Standard, hasta 5 reglas, 10 GB procesados | [Tarifa global](../../evidencias/P02/fuentes/precios_lb_global.json): 0.025/h + 0.005/GB |
| DNS | 1 zona, 100 000 consultas | Igual | [DNS](../../evidencias/P02/fuentes/precios_dns.json): tarifa pública Global, primera zona 0.50/mes, primeras consultas 0.40/millón |

La [calculadora oficial](https://azure.microsoft.com/en-us/pricing/calculator/) permitió seleccionar SQL GP con redundancia de zona en East US. El soporte regional de zonas y hardware Gen5 está descrito en [SQL reliability](https://learn.microsoft.com/en-us/azure/reliability/reliability-sql-database). East US dispone de zonas; cuota y capacidad de B2s en dos zonas de una suscripción concreta se comprobarán al desplegar. No se declara una reserva de capacidad. Functions permanece sin una mejora zonal contratada.

## Resultado

| Concepto | Base USD/mes | Redundante USD/mes |
|---|---:|---:|
| VM Linux | 30.36800 | 60.73600 |
| Discos Premium | 5.27950 | 10.55900 |
| SQL con licencia y almacenamiento | 372.97118 | 511.09698 |
| Storage | 0.70600 | 0.87250 |
| Functions bruto | 2.62000 | 2.62000 |
| IP Standard | 3.65000 | 10.95000 |
| Balanceador | 0.00000 | 18.30000 |
| DNS | 0.54000 | 0.54000 |
| Salida 10 GB dentro de franquicia | 0.00000 | 0.00000 |
| Monitor académico gratuito y logs locales | 0.00000 | 0.00000 |
| **Total** | **416.13468** | **615.67448** |
| **Incremento** | — | **199.53980** |

```text
SQL base = 0.304434 × 730 + 145.95036 + (32 + 9.6) × 0.115
         = 372.97118 USD
SQL zonal = (0.304434 + 0.18266) × 730 + 145.95036 + 41.6 × 0.23
          = 511.09698 USD
Storage base = 20 × 0.0208 + (50000/10000) × 0.05 + (100000/10000) × 0.004
             = 0.706 USD
Functions = (50000 × 2 × 1) × 0.000026 + (50000/10) × 0.000004 = 2.62 USD
```

La [página de bandwidth](https://azure.microsoft.com/en-us/pricing/details/bandwidth/) consultada el 03/10/2026 respalda la franquicia inicial de 100 GB/mes y transferencias intrarregionales sin cargo en los casos aplicables. Los 10 GB deben caber en la franquicia disponible de la suscripción; no se duplica por recurso. No hay enlace privado, NAT Gateway, Front Door ni ingestión pagada de logs. Se presupone un subdominio delegado existente y certificado TLS sin costo; la compra de un dominio nuevo no está incluida.

La [tarifa de Functions](https://azure.microsoft.com/en-us/pricing/details/functions/) incluye franquicias; se conserva el costo bruto de USD 2.62 para no confundir descuentos con garantías de SLA. El contrato excluye niveles gratuitos y compras mediante créditos de suscripción en sus condiciones. Por ello no se atribuyen estos porcentajes automáticamente a Azure for Students o a recursos cubiertos íntegramente por créditos. Es una configuración de referencia de pago, no una recomendación de gastar ese importe para esta práctica.

## Reproducción y evidencia

Desde la raíz: `python evidencias/P02/recalcular.py`. Usa `Decimal`, no consulta Internet y regenera [calculos.md](../../evidencias/P02/calculos.md) y [calculos.json](../../evidencias/P02/calculos.json). Los JSON de tarifas conservan la consulta original, fecha y medidores; [medidores utilizados](../../evidencias/P02/fuentes/medidores-utilizados.md) permite localizar los precios. No se reemplazan tarifas históricas con las del día al recalcular.

Evidencia real: [captura SQL base](../../evidencias/P02/calculadora_sql_base.jpg), [exportación oficial base](../../evidencias/P02/calculadora_sql_base.xlsx), [captura SQL redundante](../../evidencias/P02/calculadora_sql_redundante.jpg) y [lectura de configuración redundante](../../evidencias/P02/fuentes/calculadora_sql_redundante.txt). Estas capturas respaldan SQL; los demás renglones usan la API oficial guardada. No se presentan como exportación de la calculadora de toda la arquitectura.

## Alternativa de residencia en México (pregunta 3)

Escenario independiente de East US. Las siguientes cantidades son **asignaciones presupuestales hipotéticas**, no precios publicados por Google ni por un centro de datos mexicano. Sirven para exponer el orden y composición del costo de una solución candidata; no permiten contratarla.

| Partida supuesta | Cantidad y presupuesto unitario | USD/mes |
|---|---|---:|
| Aplicación en dos sitios mexicanos independientes | 4 VM × 40 | 160 |
| Nodos de datos con consenso en tres dominios mexicanos | 3 × 180 | 540 |
| Ingreso y conmutación redundantes | 2 × 50 | 100 |
| Discos, respaldos y objetos con residencia mexicana | Bolsa supuesta | 150 |
| Tráfico/enlaces entre sitios | Bolsa supuesta | 150 |
| Operación y monitorización | Bolsa supuesta | 200 |
| **Total exploratorio** | — | **1300** |

No se deduce ese total de las tarifas East US, ni se usa la tarifa aislada de una VM en México como precio de una plataforma completa. Antes de una oferta real deben verificarse proveedores/sitios, soporte de quórum y escritor único, latencia de replicación, independencia de fallas, ubicación de todas las copias y metadatos, licencias y tarifas de red. Una partición puede obligar a rechazar reservas para preservar unicidad; el SLA del cómputo no elimina esa limitación. No es correcto afirmar que dos sitios alcanzan por sí solos 99.99 %.

En la sesión previa se rechazó el acceso de navegador a precios de Google Cloud; no se obtuvo esa cotización ni se sustituyó por una cifra atribuida al proveedor. Esta limitación de evidencia permanece explícita: el requisito de un costo real verificado para México no está cerrado.
