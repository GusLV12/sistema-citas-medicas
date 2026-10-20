import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { AvailabilityCalendar, BookingStepper } from '../../components/domain/AppointmentComponents'
import { Button, Card, Field, Input, Select } from '../../components/ui'
import { api } from '../../lib/api'

export function AppointmentBookingPage() {
  const [step, setStep] = useState(1)
  const [specialtyId, setSpecialtyId] = useState('')
  const [clinicId, setClinicId] = useState('')
  const [doctorId, setDoctorId] = useState('')
  const [slotId, setSlotId] = useState('')
  const [reason, setReason] = useState('')
  const [searchParams] = useSearchParams()
  const reprogrammingId = searchParams.get('reprogramar')
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const specialties = useQuery({ queryKey: ['specialties'], queryFn: api.specialties })
  const clinics = useQuery({ queryKey: ['clinics'], queryFn: api.clinics })
  const doctors = useQuery({ queryKey: ['doctors', specialtyId, clinicId], queryFn: () => api.doctors(specialtyId, clinicId), enabled: Boolean(specialtyId && clinicId) })
  const availability = useQuery({ queryKey: ['availability', doctorId, clinicId], queryFn: () => api.availability(doctorId, clinicId), enabled: Boolean(doctorId && clinicId) })
  const mutation = useMutation({
    mutationFn: () => {
      const input = { specialtyId, doctorId, clinicId, slotId, reason }
      return reprogrammingId ? api.rescheduleAppointment(reprogrammingId, input) : api.createAppointment(input)
    },
    onSuccess: (appointment) => { queryClient.invalidateQueries({ queryKey: ['appointments'] }); navigate(`/citas/${appointment.id}`) },
  })
  const resetDoctorAndSlot = () => { setDoctorId(''); setSlotId('') }
  const specialty = specialties.data?.find((item) => item.id === specialtyId)
  const clinic = clinics.data?.find((item) => item.id === clinicId)
  const doctor = doctors.data?.find((item) => item.id === doctorId)

  return <div className="mx-auto max-w-3xl">
    <header><p className="font-semibold text-primary">{reprogrammingId ? 'Reprogramar cita' : 'Reserva de cita'}</p><h1 className="font-heading text-3xl font-extrabold">Elige un horario disponible</h1><p className="mt-2 text-muted">Conservaremos tus selecciones mientras avanzas entre los pasos.</p></header>
    <Card className="mt-6"><BookingStepper step={step} />
      {step === 1 && <div className="grid gap-4"><Field label="Especialidad"><Select value={specialtyId} onChange={(event) => { setSpecialtyId(event.target.value); setClinicId(''); resetDoctorAndSlot() }}><option value="">Selecciona una especialidad</option>{specialties.data?.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</Select></Field><div className="flex justify-end"><Button disabled={!specialtyId} onClick={() => setStep(2)}>Continuar</Button></div></div>}
      {step === 2 && <div className="grid gap-4"><Field label="Clínica"><Select value={clinicId} onChange={(event) => { setClinicId(event.target.value); resetDoctorAndSlot() }}><option value="">Selecciona una clínica</option>{clinics.data?.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</Select></Field><Field label="Médico"><Select value={doctorId} disabled={!clinicId} onChange={(event) => { setDoctorId(event.target.value); setSlotId('') }}><option value="">Selecciona un médico</option>{doctors.data?.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</Select></Field><div className="flex justify-between"><Button variant="secondary" onClick={() => setStep(1)}>Atrás</Button><Button disabled={!doctorId} onClick={() => setStep(3)}>Continuar</Button></div></div>}
      {step === 3 && <div className="grid gap-4"><p className="text-sm text-muted">Los horarios ocupados no pueden seleccionarse.</p>{availability.isLoading ? <p>Cargando horarios…</p> : <AvailabilityCalendar slots={availability.data ?? []} selected={slotId} onSelect={setSlotId} />}<div className="flex justify-between"><Button variant="secondary" onClick={() => setStep(2)}>Atrás</Button><Button disabled={!slotId} onClick={() => setStep(4)}>Continuar</Button></div></div>}
      {step === 4 && <div className="grid gap-4"><div className="rounded-md bg-slate-50 p-4 text-sm"><p><b>Especialidad:</b> {specialty?.name}</p><p><b>Médico:</b> {doctor?.name}</p><p><b>Sede:</b> {clinic?.name}</p></div><Field label="Motivo de la cita" hint="Describe brevemente el motivo de tu visita."><Input value={reason} maxLength={500} onChange={(event) => setReason(event.target.value)} /></Field>{mutation.error && <p role="alert" className="text-sm text-danger">{mutation.error.message}</p>}<div className="flex justify-between"><Button variant="secondary" onClick={() => setStep(3)}>Atrás</Button><Button disabled={mutation.isPending} onClick={() => mutation.mutate()}>{mutation.isPending ? 'Guardando…' : reprogrammingId ? 'Confirmar reprogramación' : 'Confirmar cita'}</Button></div></div>}
    </Card>
  </div>
}
