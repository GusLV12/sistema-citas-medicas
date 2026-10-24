import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Building2, CalendarClock, Stethoscope, Users } from 'lucide-react'
import { useState } from 'react'
import { Button, Card, Field, Input } from '../../components/ui'
import { api } from '../../lib/api'
import type { CreateDoctorInput } from '../../types/api'

const initialDoctor: CreateDoctorInput = { email: '', password: '', firstName: '', lastName: '', licenseNumber: '', biography: '' }

export function AdminCatalogPage() {
  const queryClient = useQueryClient()
  const specialties = useQuery({ queryKey: ['specialties'], queryFn: api.specialties })
  const clinics = useQuery({ queryKey: ['clinics'], queryFn: api.clinics })
  const doctors = useQuery({ queryKey: ['admin', 'doctors'], queryFn: api.adminDoctors })
  const users = useQuery({ queryKey: ['admin', 'users'], queryFn: api.adminUsers })
  const [doctor, setDoctor] = useState<CreateDoctorInput>(initialDoctor)
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
    <Card className="mt-6"><h2 className="font-heading text-xl font-bold">Flujo administrativo</h2><ol className="mt-3 grid gap-2 text-sm text-muted"><li>1. Crear médicos y usuarios administrativos.</li><li>2. Asociar médicos a especialidades y sedes desde los catálogos.</li><li>3. Configurar consultorios, horarios semanales y bloqueos.</li><li>4. Django valida estas relaciones antes de confirmar una cita.</li></ol></Card>
  </div>
}
