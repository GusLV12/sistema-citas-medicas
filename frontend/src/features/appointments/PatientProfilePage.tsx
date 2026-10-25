import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { Button, Card, Field, Input } from '../../components/ui'
import { api } from '../../lib/api'
import type { PatientProfile } from '../../types/api'

const empty: PatientProfile = { firstName: '', lastName: '', phone: '', birthDate: null, emergencyContactName: '', emergencyContactPhone: '' }
export function PatientProfilePage() {
  const queryClient = useQueryClient()
  const profile = useQuery({ queryKey: ['patient-profile'], queryFn: api.patientProfile })
  const [draft, setDraft] = useState<PatientProfile | null>(null)
  const form = draft ?? profile.data ?? empty
  const save = useMutation({ mutationFn: () => api.updatePatientProfile(form), onSuccess: (next) => { setDraft(next); queryClient.invalidateQueries({ queryKey: ['patient-profile'] }) } })
  const update = (field: keyof PatientProfile, value: string) => setDraft((current) => ({ ...(current ?? profile.data ?? empty), [field]: value || (field === 'birthDate' ? null : '') }))
  if (profile.isLoading) return <p className="text-muted">Cargando perfil…</p>
  if (profile.isError) return <p role="alert" className="text-danger">No se pudo cargar tu perfil. Actualiza la página para intentarlo de nuevo.</p>
  return <div className="max-w-2xl"><header><p className="font-semibold text-primary">Área de paciente</p><h1 className="font-heading text-3xl font-extrabold">Mi perfil</h1><p className="mt-2 text-muted">Mantén tus datos de contacto y contacto de emergencia actualizados.</p></header><Card className="mt-6"><form className="grid gap-4" onSubmit={(event) => { event.preventDefault(); save.mutate() }}><div className="grid gap-4 sm:grid-cols-2"><Field label="Nombre"><Input required value={form.firstName} onChange={(event) => update('firstName', event.target.value)} /></Field><Field label="Apellido"><Input required value={form.lastName} onChange={(event) => update('lastName', event.target.value)} /></Field></div><Field label="Teléfono"><Input value={form.phone} onChange={(event) => update('phone', event.target.value)} /></Field><Field label="Fecha de nacimiento"><Input type="date" value={form.birthDate ?? ''} onChange={(event) => update('birthDate', event.target.value)} /></Field><div className="border-t border-line pt-4"><h2 className="font-heading text-lg font-bold">Contacto de emergencia</h2><div className="mt-3 grid gap-4 sm:grid-cols-2"><Field label="Nombre"><Input value={form.emergencyContactName} onChange={(event) => update('emergencyContactName', event.target.value)} /></Field><Field label="Teléfono"><Input value={form.emergencyContactPhone} onChange={(event) => update('emergencyContactPhone', event.target.value)} /></Field></div></div>{save.error && <p role="alert" className="text-sm text-danger">{save.error.message}</p>}<Button type="submit" disabled={save.isPending}>{save.isPending ? 'Guardando…' : 'Guardar perfil'}</Button></form></Card></div>
}
