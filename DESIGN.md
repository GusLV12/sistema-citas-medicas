---
name: Sistema de Citas Médicas
description: Interfaz clínica, clara y accesible para pacientes, médicos y personal administrativo.
colors:
  canvas: "#F5F8FA"
  surface: "#FFFFFF"
  primary: "#0F766E"
  primaryHover: "#115E59"
  accent: "#2563EB"
  text: "#172033"
  mutedText: "#526075"
  border: "#D8E1E8"
  success: "#15803D"
  warning: "#B45309"
  danger: "#B42318"
typography:
  heading: "Manrope, sans-serif"
  body: "Inter, sans-serif"
  h1: "2rem"
  bodySize: "1rem"
spacing:
  unit: "0.25rem"
  page: "1.5rem"
  section: "2rem"
radius:
  sm: "0.375rem"
  md: "0.625rem"
  lg: "0.875rem"
---

# Dirección visual

La interfaz debe transmitir orden, calma y confianza clínica. Prioriza legibilidad, información predecible y acciones inequívocas sobre efectos decorativos. Usa un fondo azul grisáceo muy claro, superficies blancas y verde azulado como color de acción principal. El azul identifica información y enlaces; verde, ámbar y rojo expresan estados de citas sin depender únicamente del color.

## Jerarquía y composición

- La navegación distingue tres áreas: Paciente, Médico y Administración. Muestra solo las acciones permitidas por el rol actual.
- Las páginas de agenda priorizan fecha, médico, estado y hora. En móvil, usa una lista cronológica; en escritorio, usa calendario con lista alternativa accesible.
- Mantén un ancho de lectura de 72rem como máximo y una cuadrícula de 8 px. Evita tarjetas dentro de tarjetas y paneles con información repetida.
- La reserva se realiza en pasos visibles: especialidad, médico y sede, horario, confirmación. Conserva las elecciones anteriores al volver un paso.

## Componentes

- Los botones principales usan `primary`; las acciones destructivas requieren confirmación explícita y lenguaje claro.
- Los campos incluyen etiqueta persistente, ayuda contextual y error asociado al campo. No uses el texto de ejemplo como única etiqueta.
- Cada cita muestra un estado con texto, icono y color: pendiente, confirmada, cancelada, completada o inasistencia.
- Los horarios disponibles son botones con estado seleccionado; los ocupados no deben ser seleccionables ni confundirse con disponibles.
- Los estados vacíos explican qué falta y ofrecen la siguiente acción útil, por ejemplo “No tienes citas próximas” y “Reservar una cita”.

## Accesibilidad y comportamiento

- Mantén contraste de al menos 4.5:1 para texto normal y foco visible para teclado.
- Las interacciones funcionan con teclado, lector de pantalla y objetivos táctiles de al menos 44 × 44 px.
- Respeta `prefers-reduced-motion`; usa transiciones breves y funcionales, nunca animaciones que oculten cambios de estado.
- Muestra confirmación clara tras reservar, cancelar o reprogramar una cita. En errores de disponibilidad, conserva el contexto y ofrece horarios alternativos.

## Voz

Usa español claro, respetuoso y directo. Di “Reservar cita”, “Confirmar cancelación” y “No hay horarios disponibles”; evita mensajes técnicos, culpas al usuario y abreviaturas ambiguas.
