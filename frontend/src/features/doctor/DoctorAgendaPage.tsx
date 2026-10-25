import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useMemo, useState } from 'react'
import { AppointmentCard } from '../../components/domain/AppointmentComponents'
import { Button, Card, Field, Input, Select } from '../../components/ui'
import { api } from '../../lib/api'
import type { AppointmentStatus } from '../../types/api'

const statusOptions: { value: '' | AppointmentStatus; label: string }[] = [
  { value: '', label: 'Todos los estados' }, { value: 'pending', label: 'Pendiente' }, { value: 'confirmed', label: 'Confirmada' }, { value: 'completed', label: 'Completada' }, { value: 'no_show', label: 'Inasistencia' }, { value: 'cancelled', label: 'Cancelada' }, { value: 'rescheduled', label: 'Reprogramada' },
]
const isoDate = (date: Date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
const today = () => isoDate(new Date())
const startMonday = (date: Date) => { const result = new Date(date); result.setDate(result.getDate() - ((result.getDay() + 6) % 7)); return result }

export function DoctorAgendaPage() {
  const queryClient = useQueryClient()
  const [view, setView] = useState<'day' | 'week'>('day')
  const [date, setDate] = useState(today)
  const [status, setStatus] = useState<'' | AppointmentStatus>('')
  const [active, setActive] = useState<string>()
  const [summary, setSummary] = useState('')
  const range = useMemo(() => {
    const selected = new Date(`${date}T12:00:00`)
    if (view === 'day') return { date, status: status || undefined }
    const first = startMonday(selected)
    const last = new Date(first); last.setDate(first.getDate() + 6)
    return { from: isoDate(first), to: isoDate(last), status: status || undefined }
  }, [date, status, view])
  const appointments = useQuery({ queryKey: ['appointments', 'doctor', range], queryFn: () => api.appointments(range) })
  const refresh = () => queryClient.invalidateQueries({ queryKey: ['appointments'] })
  const consultation = useMutation({ mutationFn: () => api.createConsultation({ appointmentId: active!, clinicalSummary: summary }), onSuccess: () => { setActive(undefined); setSummary(''); refresh() } })
  const transition = useMutation({ mutationFn: ({ id, action }: { id: string; action: 'cancel' | 'no_show' | 'complete' }) => api.updateAppointment(id, action), onSuccess: refresh })
  return <div><header><p className="font-semibold text-primary">Área médica</p><h1 className="font-heading text-3xl font-extrabold">Mi agenda</h1><p className="mt-2 text-muted">Revisa tus citas por día o semana y registra el resultado de la atención.</p></header><Card className="mt-6"><div className="grid gap-3 sm:grid-cols-3"><Field label="Vista"><Select value={view} onChange={(event) => setView(event.target.value as 'day' | 'week')}><option value="day">Día</option><option value="week">Semana</option></Select></Field><Field label={view === 'day' ? 'Fecha' : 'Semana de referencia'}><Input type="date" value={date} onChange={(event) => setDate(event.target.value)} /></Field><Field label="Estado"><Select value={status} onChange={(event) => setStatus(event.target.value as '' | AppointmentStatus)}>{statusOptions.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}</Select></Field></div></Card>{appointments.isLoading ? <p className="mt-6 text-muted">Cargando agenda…</p> : appointments.isError ? <p role="alert" className="mt-6 text-danger">No se pudo cargar la agenda. Intenta de nuevo.</p> : <div className="mt-6 grid gap-3">{appointments.data?.length ? appointments.data.map((appointment) => <AppointmentCard key={appointment.id} appointment={appointment} actions={appointment.canWriteConsultation ? <div className="flex flex-wrap gap-2"><Button onClick={() => setActive(appointment.id)}>Registrar consulta</Button><Button variant="secondary" disabled={transition.isPending} onClick={() => transition.mutate({ id: appointment.id, action: 'no_show' })}>Inasistencia</Button><Button variant="danger" disabled={transition.isPending} onClick={() => transition.mutate({ id: appointment.id, action: 'cancel' })}>Cancelar</Button></div> : undefined} />) : <Card><p className="text-muted">No hay citas para los filtros seleccionados.</p></Card>}</div>}{active && <Card className="mt-6"><h2 className="font-heading text-xl font-bold">Resumen de consulta</h2><p className="mt-1 text-sm text-muted">Evita diagnósticos, recetas o expedientes clínicos fuera del alcance del MVP.</p><Field label="Resumen de atención"><Input value={summary} onChange={(event) => setSummary(event.target.value)} /></Field>{consultation.error && <p role="alert" className="mt-3 text-sm text-danger">{consultation.error.message}</p>}<div className="mt-4 flex gap-2"><Button variant="secondary" onClick={() => setActive(undefined)}>Cancelar</Button><Button disabled={!summary || consultation.isPending} onClick={() => consultation.mutate()}>Guardar consulta</Button></div></Card>}</div>
}
