import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Building2, CalendarClock, Stethoscope, Users } from 'lucide-react'
import { useState } from 'react'
import { Button, Card, Field, Input, Select } from '../../components/ui'
import { api } from '../../lib/api'
import type { CatalogRecord, CreateDoctorInput } from '../../types/api'

const initialDoctor: CreateDoctorInput = { email: '', password: '', firstName: '', lastName: '', licenseNumber: '', biography: '' }
type CatalogName = 'specialties' | 'clinics' | 'rooms' | 'doctor-specialties' | 'doctor-clinics' | 'availability-rules' | 'unavailabilities'
type CatalogField = { name: string; label: string; type?: 'text' | 'number' | 'time' | 'date' | 'datetime-local' | 'select'; options?: () => { value: string; label: string }[] }

const catalogLabels: Record<CatalogName, string> = { specialties: 'Especialidades', clinics: 'Clínicas', rooms: 'Consultorios', 'doctor-specialties': 'Especialidades por médico', 'doctor-clinics': 'Clínicas por médico', 'availability-rules': 'Horarios recurrentes', unavailabilities: 'Bloqueos puntuales' }

export function AdminCatalogPage() {
  const queryClient = useQueryClient()
  const specialties = useQuery({ queryKey: ['specialties'], queryFn: api.specialties })
  const clinics = useQuery({ queryKey: ['clinics'], queryFn: api.clinics })
  const doctors = useQuery({ queryKey: ['admin', 'doctors'], queryFn: api.adminDoctors })
  const users = useQuery({ queryKey: ['admin', 'users'], queryFn: api.adminUsers })
  const adminSpecialties = useQuery({ queryKey: ['admin-catalog', 'specialties'], queryFn: () => api.adminCatalog<CatalogRecord>('specialties') })
  const adminClinics = useQuery({ queryKey: ['admin-catalog', 'clinics'], queryFn: () => api.adminCatalog<CatalogRecord>('clinics') })
  const rooms = useQuery({ queryKey: ['admin-catalog', 'rooms'], queryFn: () => api.adminCatalog<CatalogRecord>('rooms') })
  const doctorSpecialties = useQuery({ queryKey: ['admin-catalog', 'doctor-specialties'], queryFn: () => api.adminCatalog<CatalogRecord>('doctor-specialties') })
  const doctorClinics = useQuery({ queryKey: ['admin-catalog', 'doctor-clinics'], queryFn: () => api.adminCatalog<CatalogRecord>('doctor-clinics') })
  const rules = useQuery({ queryKey: ['admin-catalog', 'availability-rules'], queryFn: () => api.adminCatalog<CatalogRecord>('availability-rules') })
  const unavailabilities = useQuery({ queryKey: ['admin-catalog', 'unavailabilities'], queryFn: () => api.adminCatalog<CatalogRecord>('unavailabilities') })
  const [doctor, setDoctor] = useState<CreateDoctorInput>(initialDoctor)
  const [catalog, setCatalog] = useState<CatalogName>('specialties')
  const [draft, setDraft] = useState<Record<string, string>>({})
  const createDoctor = useMutation({
    mutationFn: () => api.createDoctor(doctor),
    onSuccess: () => {
      setDoctor(initialDoctor)
      queryClient.invalidateQueries({ queryKey: ['admin', 'doctors'] })
      queryClient.invalidateQueries({ queryKey: ['admin', 'users'] })
    },
  })
  const updateUser = useMutation({
    mutationFn: ({ id, isActive }: { id: string; isActive: boolean }) => api.updateAdminUser(id, { isActive }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin', 'users'] }),
  })
  const catalogData: Record<CatalogName, CatalogRecord[]> = { specialties: adminSpecialties.data ?? [], clinics: adminClinics.data ?? [], rooms: rooms.data ?? [], 'doctor-specialties': doctorSpecialties.data ?? [], 'doctor-clinics': doctorClinics.data ?? [], 'availability-rules': rules.data ?? [], unavailabilities: unavailabilities.data ?? [] }
  const doctorOptions = () => (doctors.data ?? []).map((item) => ({ value: item.id, label: `${item.firstName} ${item.lastName}` }))
  const clinicOptions = () => catalogData.clinics.map((item) => ({ value: String(item.id), label: String(item.name) }))
  const specialtyOptions = () => catalogData.specialties.map((item) => ({ value: String(item.id), label: String(item.name) }))
  const doctorClinicOptions = () => catalogData['doctor-clinics'].map((item) => ({ value: String(item.id), label: `${String(item.doctor)} · ${String(item.clinic)}` }))
  const fields: Record<CatalogName, CatalogField[]> = {
    specialties: [{ name: 'name', label: 'Nombre' }, { name: 'description', label: 'Descripción' }],
    clinics: [{ name: 'name', label: 'Nombre' }, { name: 'address', label: 'Dirección' }, { name: 'phone', label: 'Teléfono' }, { name: 'timezone', label: 'Zona horaria' }],
    rooms: [{ name: 'clinic', label: 'Clínica', type: 'select', options: clinicOptions }, { name: 'code', label: 'Código' }, { name: 'name', label: 'Nombre visible' }],
    'doctor-specialties': [{ name: 'doctor', label: 'Médico', type: 'select', options: doctorOptions }, { name: 'specialty', label: 'Especialidad', type: 'select', options: specialtyOptions }],
    'doctor-clinics': [{ name: 'doctor', label: 'Médico', type: 'select', options: doctorOptions }, { name: 'clinic', label: 'Clínica', type: 'select', options: clinicOptions }],
    'availability-rules': [{ name: 'doctor_clinic', label: 'Médico y clínica', type: 'select', options: doctorClinicOptions }, { name: 'weekday', label: 'Día (0 lunes, 6 domingo)', type: 'number' }, { name: 'starts_at', label: 'Desde', type: 'time' }, { name: 'ends_at', label: 'Hasta', type: 'time' }, { name: 'slot_minutes', label: 'Duración de cita', type: 'number' }],
    unavailabilities: [{ name: 'doctor_clinic', label: 'Médico y clínica', type: 'select', options: doctorClinicOptions }, { name: 'starts_at', label: 'Inicia', type: 'datetime-local' }, { name: 'ends_at', label: 'Termina', type: 'datetime-local' }, { name: 'reason', label: 'Motivo' }],
  }
  const createCatalog = useMutation({ mutationFn: () => api.createAdminCatalog<CatalogRecord>(catalog, Object.fromEntries(Object.entries(draft).map(([key, value]) => [key, ['weekday', 'slot_minutes'].includes(key) ? Number(value) : value]))), onSuccess: () => { setDraft({}); queryClient.invalidateQueries({ queryKey: ['admin-catalog', catalog] }); queryClient.invalidateQueries({ queryKey: ['specialties'] }); queryClient.invalidateQueries({ queryKey: ['clinics'] }) } })
  const deactivateCatalog = useMutation({ mutationFn: ({ resource, id }: { resource: CatalogName; id: string }) => api.updateAdminCatalog<CatalogRecord>(resource, id, { is_active: false }), onSuccess: (_, variables) => queryClient.invalidateQueries({ queryKey: ['admin-catalog', variables.resource] }) })
  const items = [
    { label: 'Especialidades', value: specialties.data?.length ?? '—', icon: Stethoscope },
    { label: 'Clínicas', value: clinics.data?.length ?? '—', icon: Building2 },
    { label: 'Médicos activos', value: doctors.data?.filter((item) => item.isActive).length ?? '—', icon: Users },
    { label: 'Disponibilidad', value: 'Reglas semanales', icon: CalendarClock },
  ]
  const update = (field: keyof CreateDoctorInput, value: string) => setDoctor((current) => ({ ...current, [field]: value }))

  return <div>
    <header><p className="font-semibold text-primary">Administración</p><h1 className="font-heading text-3xl font-extrabold">Configuración de la clínica</h1><p className="mt-2 text-muted">Gestiona los usuarios, médicos y catálogos que determinan la disponibilidad.</p></header>
    <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{items.map(({ label, value, icon: Icon }) => <Card key={label}><Icon className="text-primary" size={22} /><p className="mt-4 text-sm font-semibold text-muted">{label}</p><p className="mt-1 font-heading text-xl font-extrabold">{value}</p></Card>)}</div>
    <div className="mt-6 grid gap-6 lg:grid-cols-2">
      <Card><h2 className="font-heading text-xl font-bold">Alta de médico</h2><form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); createDoctor.mutate() }}><div className="grid gap-3 sm:grid-cols-2"><Field label="Nombre"><Input required value={doctor.firstName} onChange={(event) => update('firstName', event.target.value)} /></Field><Field label="Apellido"><Input required value={doctor.lastName} onChange={(event) => update('lastName', event.target.value)} /></Field></div><Field label="Correo"><Input required type="email" value={doctor.email} onChange={(event) => update('email', event.target.value)} /></Field><Field label="Cédula profesional"><Input required value={doctor.licenseNumber} onChange={(event) => update('licenseNumber', event.target.value)} /></Field><Field label="Contraseña temporal"><Input required minLength={8} type="password" value={doctor.password} onChange={(event) => update('password', event.target.value)} /></Field>{createDoctor.error && <p role="alert" className="text-sm text-danger">{createDoctor.error.message}</p>}<Button type="submit" disabled={createDoctor.isPending}>{createDoctor.isPending ? 'Creando…' : 'Crear médico'}</Button></form></Card>
      <Card><h2 className="font-heading text-xl font-bold">Usuarios</h2><div className="mt-4 grid gap-2">{users.data?.map((user) => <div key={user.id} className="flex items-center justify-between gap-3 rounded-md border border-line p-3 text-sm"><div><p className="font-semibold">{user.name}</p><p className="text-muted">{user.email} · {user.role} · {user.isActive ? 'Activo' : 'Inactivo'}</p></div><Button variant="secondary" disabled={updateUser.isPending} onClick={() => updateUser.mutate({ id: user.id, isActive: !user.isActive })}>{user.isActive ? 'Desactivar' : 'Activar'}</Button></div>) ?? <p className="text-muted">Cargando usuarios…</p>}</div></Card>
    </div>
    <Card className="mt-6"><div className="flex flex-wrap items-end justify-between gap-3"><div><h2 className="font-heading text-xl font-bold">Operación clínica</h2><p className="mt-1 text-sm text-muted">Configura la oferta que verá el paciente al reservar.</p></div><label className="grid gap-1 text-sm font-semibold">Catálogo<Select value={catalog} onChange={(event) => { setCatalog(event.target.value as CatalogName); setDraft({}) }}>{(Object.keys(catalogLabels) as CatalogName[]).map((name) => <option key={name} value={name}>{catalogLabels[name]}</option>)}</Select></label></div><form className="mt-5 grid gap-3 sm:grid-cols-2" onSubmit={(event) => { event.preventDefault(); createCatalog.mutate() }}>{fields[catalog].map((field) => <Field key={field.name} label={field.label}>{field.type === 'select' ? <Select required value={draft[field.name] ?? ''} onChange={(event) => setDraft((value) => ({ ...value, [field.name]: event.target.value }))}><option value="">Selecciona…</option>{field.options?.().map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</Select> : <Input required={field.name !== 'description' && field.name !== 'phone' && field.name !== 'reason'} type={field.type ?? 'text'} value={draft[field.name] ?? ''} onChange={(event) => setDraft((value) => ({ ...value, [field.name]: event.target.value }))} />}</Field>)}{createCatalog.error && <p role="alert" className="sm:col-span-2 text-sm text-danger">{createCatalog.error.message}</p>}<div className="sm:col-span-2"><Button type="submit" disabled={createCatalog.isPending}>{createCatalog.isPending ? 'Guardando…' : `Agregar ${catalogLabels[catalog].toLowerCase()}`}</Button></div></form><div className="mt-6 grid gap-2">{catalogData[catalog].length ? catalogData[catalog].map((item) => <div key={item.id} className="flex items-center justify-between gap-3 rounded-md border border-line p-3 text-sm"><p className="min-w-0 break-words text-muted">{Object.entries(item).filter(([key]) => !['id', 'created_at', 'updated_at'].includes(key)).map(([key, value]) => `${key}: ${String(value)}`).join(' · ')}</p>{('is_active' in item) && item.is_active !== false && <Button variant="secondary" disabled={deactivateCatalog.isPending} onClick={() => deactivateCatalog.mutate({ resource: catalog, id: item.id })}>Desactivar</Button>}</div>) : <p className="text-sm text-muted">Aún no hay registros en este catálogo.</p>}</div></Card>
  </div>
}
