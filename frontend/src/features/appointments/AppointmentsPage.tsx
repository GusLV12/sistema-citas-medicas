import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { AppointmentCard } from '../../components/domain/AppointmentComponents'
import { Button, Dialog, DialogClose, EmptyState } from '../../components/ui'
import { api } from '../../lib/api'
import { canPatientChange } from '../../lib/utils'

export function AppointmentsPage() {
  const queryClient = useQueryClient()
  const { data: appointments = [], isLoading } = useQuery({ queryKey: ['appointments', 'patient'], queryFn: api.appointments })
  const mutation = useMutation({ mutationFn: (id: string) => api.updateAppointment(id, 'cancel'), onSuccess: () => queryClient.invalidateQueries({ queryKey: ['appointments'] }) })
  if (isLoading) return <p>Cargando citas…</p>
  if (!appointments.length) return <EmptyState title="No tienes citas" description="Reserva una cita cuando necesites atención." action={<Link className="inline-flex min-h-11 items-center rounded-md bg-primary px-4 font-semibold text-white" to="/paciente/reservar">Reservar cita</Link>} />
  return <div><header><p className="font-semibold text-primary">Área de paciente</p><h1 className="font-heading text-3xl font-extrabold">Mis citas</h1><p className="mt-2 text-muted">Puedes cancelar o reprogramar hasta 24 horas antes.</p></header><div className="mt-6 grid gap-3">{appointments.map((appointment) => {
    const editable = ['pending', 'confirmed'].includes(appointment.status) && canPatientChange(appointment.startsAt)
    return <AppointmentCard key={appointment.id} appointment={appointment} actions={<><Link className="min-h-11 px-2 py-2 font-semibold text-primary underline" to={`/citas/${appointment.id}`}>Detalle</Link>{editable && <Link className="min-h-11 px-2 py-2 font-semibold text-primary underline" to={`/paciente/reservar?reprogramar=${appointment.id}`}>Reprogramar</Link>}{editable ? <Dialog title="Confirmar cancelación" description="La cita quedará cancelada y conservará su historial." trigger={<Button variant="danger">Cancelar</Button>}><div className="flex justify-end gap-2"><DialogClose><Button variant="secondary">Volver</Button></DialogClose><Button variant="danger" onClick={() => mutation.mutate(appointment.id)}>Confirmar cancelación</Button></div></Dialog> : <span className="max-w-52 text-sm text-muted">Para cambios con menos de 24 h, contacta a la clínica.</span>}</>} />
  })}</div></div>
}
