# Evidencias de P02

Consulta de fuentes: 03/10/2026. [Reporte](../../practicas/P02/README.md) · [costos](../../practicas/P02/costos.md) · [arquitectura](../../docs/arquitectura/arquitectura-p02.md).

## Contratos

Las PNG corresponden al documento oficial español, edición 01/09/2026. La portada muestra la fecha y cada conjunto contiene la cláusula del servicio correspondiente. Los identificadores Alumno2/Alumno3 se actualizarán con los datos del equipo.

| Evidencia | Archivos | Qué respalda |
|---|---|---|
| Encabezado y condiciones | [Portada](P02_B1_Portada.png), [términos](P02_B1_Terminos.png), [exclusiones](P02_B1_Exclusiones.png) | Proveedor, edición, periodo, reclamación y límites comunes |
| VM | [1](P02_B1_VM_GustavoLinares.png), [2](P02_B1_VM_GustavoLinares_2.png), [3](P02_B1_VM_GustavoLinares_3.png) | Configuración por discos, Availability Set y zonas; escalones |
| SQL | [1](P02_B1_SQL_Alumno2.png), [2](P02_B1_SQL_Alumno2_2.png) | Disponibilidad y redundancia; contrastar omisión de GP en español con inglés |
| Blob | [1](P02_B1_Blob_Alumno3.png), [2](P02_B1_Blob_Alumno3_2.png), [3](P02_B1_Blob_Alumno3_3.png) | Storage Accounts: tasas, transacciones y escalones |
| Functions | [1](P02_B1_Functions_GustavoLinares.png), [2](P02_B1_Functions_GustavoLinares_2.png) | Diferencia Consumption/Flex y créditos |
| Balanceador | [SLA](P02_B1_LoadBalancer.png) | Condiciones de Standard con dos VM saludables |

Los [extractos en inglés](fuentes/extractos-sla.md) incluyen DNS y los cuatro servicios. Cada integrante debe conservar su captura del SLA y confirmar el nombre de archivo.

## Documentación de la arquitectura Azure

| Servicio | Captura oficial | Aspecto mostrado |
|---|---|---|
| Virtual Machines | [VM](P02_B1_VM_GustavoLinares_web.jpg) | Opciones de disponibilidad y zonas |
| SQL Database | [SQL General Purpose](P02_B1_SQL_Alumno2_web.jpg) | Nivel General Purpose seleccionado |
| Blob Storage | [Storage](P02_B1_Blob_Alumno3_web.jpg) | Redundancia de Azure Storage |
| Functions | [Functions Flex](P02_B1_Functions_GustavoLinares_web.jpg) | Plan Flex Consumption seleccionado |

## Costos y cálculos

- [Calculadora de precios de Azure](https://azure.microsoft.com/en-us/pricing/calculator/): reproducir SQL base y redundante con los supuestos de [costos](../../practicas/P02/costos.md).
- [Precios de Azure SQL Database](https://azure.microsoft.com/en-us/pricing/details/azure-sql-database/single/): consultar tarifas y opciones de SQL.
- [Cálculos completos](calculos.md) y [resultados JSON](calculos.json).
- [Medidores usados](fuentes/medidores-utilizados.md), con referencia a los JSON oficiales que conservan URL y fecha. `precios_lb.json` es la respuesta vacía del filtro regional descartado; la tarifa utilizada es `precios_lb_global.json`.
- [Diagrama definitivo](../../docs/arquitectura/arquitectura-p02.md), en Mermaid con leyenda de flujos.

Las fórmulas de disponibilidad y costo están disponibles en Markdown.

## Plan de medición

El plan de medición se encuentra en [SLO](../../docs/slo.md). El monitor de 24 horas es un elemento opcional de la práctica.
