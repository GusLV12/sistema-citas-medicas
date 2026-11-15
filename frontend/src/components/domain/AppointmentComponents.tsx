import { CalendarDays, Clock } from 'lucide-react'
import type { ReactNode } from 'react'
import type { Appointment, AppointmentStatus, AvailabilitySlot } from '../../types/api'
import { formatDateTime, cn } from '../../lib/utils'

const statusStyle: Record<AppointmentStatus, string> = { pending: 'bg-amber-100 text-warning', confirmed: 'bg-teal-100 text-primary', cancelled: 'bg-red-100 text-danger', completed: 'bg-green-100 text-success', no_show: 'bg-slate-200 text-slate-700', rescheduled: 'bg-blue-100 text-accent' }
const statusLabel: Record<AppointmentStatus, string> = { pending: 'Pendiente', confirmed: 'Confirmada', cancelled: 'Cancelada', completed: 'Completada', no_show: 'Inasistencia', rescheduled: 'Reprogramada' }
export const AppointmentStatusBadge = ({ status }: { status: AppointmentStatus }) => <span className={cn('inline-flex h-fit items-center self-start whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-bold', statusStyle[status])}>{statusLabel[status]}</span>
export function AppointmentCard({ appointment, actions }: { appointment: Appointment; actions?: ReactNode }) { return <article className="flex flex-col gap-4 rounded-lg border border-line bg-white p-4 sm:flex-row sm:items-center sm:justify-between"><div><div className="flex flex-wrap items-center gap-2"><h3 className="font-heading font-bold">{appointment.specialty} · {appointment.doctorName}</h3><AppointmentStatusBadge status={appointment.status} /></div><p className="mt-1 flex items-center gap-1 text-sm text-muted"><CalendarDays size={15} />{appointment.clinic}</p><p className="mt-1 flex items-center gap-1 text-sm text-muted"><Clock size={15} />{formatDateTime(appointment.startsAt)}</p></div>{actions && <div className="flex flex-wrap gap-2">{actions}</div>}</article> }
export function SlotButton({ slot, selected, onSelect }: { slot: AvailabilitySlot; selected: boolean; onSelect: () => void }) { return <button type="button" disabled={!slot.available} aria-pressed={selected} onClick={onSelect} className={cn('min-h-11 rounded-md border px-3 font-semibold', selected ? 'border-primary bg-teal-50 text-primary' : 'border-line bg-white', !slot.available && 'cursor-not-allowed bg-slate-100 text-slate-400 line-through')}>{new Intl.DateTimeFormat('es-MX', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' }).format(new Date(slot.startsAt))}</button> }
export function BookingStepper({ step }: { step: number }) { return <ol className="mb-6 grid grid-cols-4 gap-2 text-center text-xs font-semibold text-muted">{['Especialidad', 'Médico y sede', 'Horario', 'Confirmación'].map((name, index) => <li key={name} className={cn('border-t-4 pt-2', index + 1 <= step ? 'border-primary text-primary' : 'border-line')}>{name}</li>)}</ol> }
const ZONE = 'America/Mexico_City'
const dayKey = (value: string) => new Intl.DateTimeFormat('en-CA', { timeZone: ZONE }).format(new Date(value))
const dayLabel = (value: string) => new Intl.DateTimeFormat('es-MX', { weekday: 'long', day: 'numeric', month: 'long', timeZone: ZONE }).format(new Date(value))
export function AvailabilityCalendar({ slots, selected, onSelect }: { slots: AvailabilitySlot[]; selected?: string; onSelect: (id: string) => void }) {
  const days = slots.reduce<{ key: string; label: string; slots: AvailabilitySlot[] }[]>((groups, slot) => {
    const key = dayKey(slot.startsAt)
    const group = groups.find((item) => item.key === key)
    if (group) group.slots.push(slot)
    else groups.push({ key, label: dayLabel(slot.startsAt), slots: [slot] })
    return groups
  }, [])
  if (!days.length) return <p className="text-sm text-muted">No hay horarios disponibles en los próximos días.</p>
  return <div className="grid gap-5">{days.map((day) => <div key={day.key}><h3 className="mb-2 text-sm font-bold text-ink first-letter:uppercase">{day.label}</h3><div className="grid grid-cols-3 gap-2 sm:grid-cols-5">{day.slots.map((slot) => <SlotButton key={slot.id} slot={slot} selected={selected === slot.id} onSelect={() => onSelect(slot.id)} />)}</div></div>)}</div>
}
