"""Reproduce costos y disponibilidad sin red ni dependencias externas."""
from decimal import Decimal as D
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
H=D(730); M=D(43200)
def prod(*xs):
    a=D(1)
    for x in xs: a*=D(str(x))
    return a
flows={
 'agenda_base':prod(1,.999,.9999),
 'agenda_vm_az':prod(1,.9999,.9999,.9999),
 'agenda_sql_zr':prod(1,.999,.99995),
 'agenda_redundante':prod(1,.9999,.9999,.99995),
 'comprobante_base':prod(.9999,.9995,.999),
 'comprobante_redundante':prod(.99995,.9995,.999),
 'reserva_y_comprobante_base':prod(1,.999,.9999,.9995,.999),
 'reserva_y_comprobante_redundante':prod(1,.9999,.9999,.99995,.9995,.999),
}
# SQL: tarifa de cómputo API + licencia comprobada en exportación oficial + datos y logs.
sql_base=D('.304434')*H+D('145.95036')+D('41.6')*D('.115')
sql_zr=(D('.304434')+D('.18266'))*H+D('145.95036')+D('41.6')*D('.23')
rows=[
 ('VM B2s Linux',D('.0416')*H,D('.0416')*H*2),
 ('Disco SO Premium SSD P4 LRS 32 GiB',D('5.2795'),D('5.2795')*2),
 ('SQL GP Gen5 2 vCore con licencia y 32 GB datos + 9.6 GB log',sql_base,sql_zr),
 ('Blob GPv2 Hot 20 GB + 50000 escrituras + 100000 lecturas',D(20)*D('.0208')+5*D('.05')+10*D('.004'),D(20)*D('.026')+5*D('.0625')+10*D('.004')),
 ('Functions Flex 50000 ejecuciones de 2 GB por 1 s, importe bruto',D(100000)*D('.000026')+D(50000)/10*D('.000004'),D(100000)*D('.000026')+D(50000)/10*D('.000004')),
 ('IP pública Standard (1 base; 1 frontend + 2 salida redundante)',D('.005')*H,D('.005')*H*3),
 ('Load Balancer Standard hasta 5 reglas + 10 GB',D(0),D('.025')*H+D(10)*D('.005')),
 ('Azure DNS público 1 zona y 100000 consultas',D('.5')+D('.4')/10,D('.5')+D('.4')/10),
 ('Salida a Internet 10 GB dentro de 100 GB gratuitos',D(0),D(0)),
 ('Logs locales y monitor gratuito; sin ingestión pagada',D(0),D(0)),
]
base=sum(r[1] for r in rows); red=sum(r[2] for r in rows)
result={'horas_costos':730,'minutos_ventana_slo':43200,'flujos':{k:{'disponibilidad_pct':str(v*100),'minutos':str((1-v)*M)} for k,v in flows.items()},'costos':{'base':str(base),'redundante':str(red),'incremento':str(red-base),'sql_base':str(sql_base),'sql_redundante':str(sql_zr)},'mejoras':{'vm_az_costo_extra':str(D('.0416')*H+D('5.2795')+2*D('.005')*H+D('.025')*H+D('.05')),'sql_zr_costo_extra':str(sql_zr-sql_base)},'presupuestos':{'disponibilidad':str(D('.005')*M),'latencia':str(D('.05')*M)}}
(ROOT/'calculos.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
md=['# Cálculos reproducibles de P02','','Generado con `python evidencias/P02/recalcular.py`. Tarifas consultadas el 03/10/2026; no son una factura.','','## Disponibilidad','','| Flujo | Disponibilidad % | Minutos equivalentes / 30 días |','|---|---:|---:|']
for k,v in flows.items(): md.append(f'| {k} | {v*100:.8f} | {(1-v)*M:.5f} |')
md+=['','## Costos en USD por mes de 730 horas','','| Concepto | Base | Redundante | Incremento |','|---|---:|---:|---:|']
for label,b,r in rows: md.append(f'| {label} | {b:.5f} | {r:.5f} | {r-b:.5f} |')
md.append(f'| **Total** | **{base:.5f}** | **{red:.5f}** | **{red-base:.5f}** |')
md+=['','## Presupuestos y crédito','','Disponibilidad: 0.005 × 43200 = 216 min equivalentes. Alertas: 108 / 216.','Latencia: 0.05 × 43200 = 2160 min equivalentes. Alertas: 1080 / 2160.','Estos presupuestos se consumen por eventos, no por cronómetro: errores / (fracción permitida × solicitudes válidas).',f'Caída hipotética VM de 8 h: disponibilidad 98.88888889%; crédito 25% × {D(".0416")*H:.3f} USD = {D(".25")*D(".0416")*H:.3f} USD.','Incidente AFD, duración global 504 min: 504/216 × 100 = 233.3333% del presupuesto temporal equivalente, solo si la aplicación hubiera fallado durante todo el intervalo.']
md += ['', '## Tabla 1: minutos y crédito a exactamente 99.0 %', '', 'Umbrales estrictos; se elige el escalón más alto aplicable. Los minutos convierten porcentajes a 30 días y no reemplazan la métrica contractual de Storage o Consumption.', '', '| Configuración | Objetivo % | Minutos equivalentes | Crédito sobre USD 100 |', '|---|---:|---:|---:|']
contracts = [
 ('VM Premium', '99.9', [('99.9',10),('99',25),('95',100)]),
 ('VM Standard SSD', '99.5', [('99.5',10),('95',25),('90',100)]),
 ('VM Standard HDD', '95', [('95',10),('92',25),('90',100)]),
 ('VM Availability Set', '99.95', [('99.95',10),('99',25),('95',100)]),
 ('VM entre zonas', '99.99', [('99.99',10),('99',25),('95',100)]),
 ('SQL sin zonas / Basic / Standard', '99.99', [('99.99',10),('99',25),('95',100)]),
 ('SQL con zonas GP / BC / Premium / Hyperscale', '99.995', [('99.995',10),('99',25),('95',100)]),
 ('Blob Hot ordinario y escrituras RA', '99.9', [('99.9',10),('99',25)]),
 ('Blob Hot lecturas RA', '99.99', [('99.99',10),('99',25)]),
 ('Functions Consumption / Flex / Premium / Dedicated', '99.95', [('99.95',10),('99',25),('95',100)]),
 ('DNS', '100', [('100',10),('99.99',25),('99.5',100)]),
 ('Load Balancer Standard', '99.99', [('99.99',10),('99.9',25)]),
]
for name,target,tiers in contracts:
    credit = max([pct for threshold,pct in tiers if D('99.0') < D(threshold)], default=0)
    md.append(f'| {name} | {target} | {(1-D(target)/100)*M:.2f} | USD {credit:.2f} |')
md += ['', '## Escenarios de las preguntas', '', 'Ocho horas: ingreso potencial perdido = 8 × 4 reservas/h × USD 25 × 50 % no recuperado = USD 400; USD 7.592 / USD 400 = 1.898 %.', '80 % del presupuesto temporal de disponibilidad: 172.8 min consumidos, 43.2 min restantes.', 'México (supuestos, no garantía): 0.9995² × 100 = 99.900025 %; [1 − (1 − 0.9995)²] × 0.99995 × 100 = 99.99497500125 %.', 'Presupuesto exploratorio México = 160 + 540 + 100 + 150 + 150 + 200 = USD 1300/mes. No es cotización.', 'Los flujos reserva_y_comprobante son una comparación de exigir ambos éxitos; no definen el SLO de agenda ni una entrega instantánea del trabajo asíncrono.']
(ROOT/'calculos.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
assert flows['agenda_base']>D('.995')
assert flows['agenda_redundante']>flows['agenda_base']
assert sql_base==D('372.97118')
assert sql_zr==D('511.09698')
assert (1-D('.995'))*M==216
print(json.dumps(result,ensure_ascii=False,indent=2))
