import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { AppointmentStatusBadge } from '../../components/domain/AppointmentComponents'
import { Button, Card, EmptyState } from '../../components/ui'
import { api } from '../../lib/api'
import { canPatientChange, formatDateTime } from '../../lib/utils'
import { useAuth } from '../auth/useAuth'

export function AppointmentDetailPage() {
  const { appointmentId } = useParams()
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const { data: appointments = [] } = useQuery({ queryKey: ['appointments', user?.role], queryFn: () => api.appointments() })
  const appointment = appointments.find((item) => item.id === appointmentId)
  const cancel = useMutation({ mutationFn: () => api.updateAppointment(appointmentId!, 'cancel'), onSuccess: () => queryClient.invalidateQueries({ queryKey: ['appointments'] }) })
  const backTo = user?.role === 'doctor' ? '/medico' : '/paciente/citas'
  if (!appointment) return <EmptyState title="Cita no encontrada" description="La cita pudo haber cambiado o no tienes permiso para verla." action={<Link className="inline-flex min-h-11 items-center rounded-md bg-primary px-4 font-semibold text-white" to={backTo}>Volver</Link>} />
  const patientCanChange = user?.role === 'patient' && ['pending', 'confirmed'].includes(appointment.status) && canPatientChange(appointment.startsAt)
  return <div className="mx-auto max-w-2xl"><Link className="font-semibold text-primary underline print:hidden" to={backTo}>← Volver</Link><Card className="mt-4"><div className="flex flex-wrap justify-between gap-3"><div><p className="font-semibold text-primary">Constancia de cita</p><h1 className="font-heading text-2xl font-extrabold">{appointment.specialty}</h1></div><AppointmentStatusBadge status={appointment.status} /></div><dl className="mt-6 grid gap-4 text-sm sm:grid-cols-2"><div><dt className="text-muted">Médico</dt><dd className="font-semibold">{appointment.doctorName}</dd></div><div><dt className="text-muted">Clínica</dt><dd className="font-semibold">{appointment.clinic}</dd></div><div><dt className="text-muted">Fecha y hora</dt><dd className="font-semibold">{formatDateTime(appointment.startsAt)}</dd></div><div><dt className="text-muted">Motivo</dt><dd className="font-semibold">{appointment.reason || 'Sin motivo especificado'}</dd></div>{appointment.cancellationReason && <div className="sm:col-span-2"><dt className="text-muted">Motivo de cancelación</dt><dd className="font-semibold">{appointment.cancellationReason}</dd></div>}</dl><div className="mt-6 print:hidden"><Button variant="secondary" onClick={() => window.print()}>Imprimir constancia</Button></div>{patientCanChange && <div className="mt-6 flex flex-wrap gap-2 print:hidden"><Link className="inline-flex min-h-11 items-center rounded-md border border-line bg-white px-4 font-semibold text-ink" to={`/paciente/reservar?reprogramar=${appointment.id}`}>Reprogramar cita</Link><Button variant="danger" disabled={cancel.isPending} onClick={() => cancel.mutate()}>Cancelar cita</Button></div>}{cancel.error && <p role="alert" className="mt-3 text-sm text-danger">{cancel.error.message}</p>}{user?.role === 'patient' && !patientCanChange && ['pending', 'confirmed'].includes(appointment.status) && <p className="mt-6 rounded-md bg-amber-50 p-3 text-sm text-warning">Faltan menos de 24 horas. Contacta a la clínica para realizar cambios.</p>}</Card></div>
}
