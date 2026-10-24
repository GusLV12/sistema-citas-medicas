import { http, HttpResponse } from 'msw'
import type { Appointment, AppointmentStatus, Clinic, Doctor, Specialty, User, UserRole } from '../types/api'

const inDays = (days: number, hour: number) => { const value = new Date(); value.setDate(value.getDate() + days); value.setHours(hour, 0, 0, 0); return value.toISOString() }
const users: Record<UserRole, User> = { patient: { id: 'patient-1', name: 'Ana López', email: 'paciente@salud.mx', role: 'patient' }, doctor: { id: 'doctor-1', name: 'Dra. Sofía Ramos', email: 'medico@salud.mx', role: 'doctor' }, admin: { id: 'admin-1', name: 'Mariana Cruz', email: 'admin@salud.mx', role: 'admin' } }
const specialties: Specialty[] = [{ id: 'cardiology', name: 'Cardiología', description: 'Atención cardiovascular.' }, { id: 'general', name: 'Medicina general', description: 'Consulta de atención primaria.' }, { id: 'dermatology', name: 'Dermatología', description: 'Atención de piel y cabello.' }]
const clinics: Clinic[] = [{ id: 'centro', name: 'Clínica Centro', address: 'Av. Reforma 120, Ciudad de México' }, { id: 'norte', name: 'Clínica Norte', address: 'Av. Insurgentes 450, Ciudad de México' }]
const doctors: Doctor[] = [{ id: 'doctor-1', name: 'Dra. Sofía Ramos', specialtyIds: ['cardiology', 'general'], clinicIds: ['centro'] }, { id: 'doctor-2', name: 'Dr. Diego Torres', specialtyIds: ['dermatology'], clinicIds: ['norte', 'centro'] }]
let adminDoctors = [{ id: 'doctor-1', email: 'medico@salud.mx', firstName: 'Sofía', lastName: 'Ramos', licenseNumber: 'CED-001', biography: '', isActive: true, defaultAppointmentMinutes: 30 }]
let appointments: Appointment[] = [{ id: 'appointment-1', patientName: 'Ana López', doctorName: 'Dra. Sofía Ramos', doctorId: 'doctor-1', specialty: 'Cardiología', clinic: 'Clínica Centro', startsAt: inDays(3, 10), endsAt: inDays(3, 11), status: 'confirmed', reason: 'Revisión de seguimiento' }, { id: 'appointment-2', patientName: 'Ana López', doctorName: 'Dra. Sofía Ramos', doctorId: 'doctor-1', specialty: 'Medicina general', clinic: 'Clínica Centro', startsAt: inDays(1, 9), endsAt: inDays(1, 10), status: 'pending', reason: 'Consulta preventiva' }]
const roleOf = (request: Request): UserRole => (request.headers.get('X-Demo-Role') as UserRole) || 'patient'
const response = (data: unknown, init?: ResponseInit) => HttpResponse.json(data as never, init)

export const handlers = [
  http.post('/api/v1/auth/login', async ({ request }) => { const { email } = await request.json() as { email: string }; const user = email.includes('medico') ? users.doctor : email.includes('admin') ? users.admin : users.patient; return response(user) }),
  http.post('/api/v1/auth/register', async ({ request }) => { const { name, email } = await request.json() as { name: string; email: string }; return response({ id: crypto.randomUUID(), name, email, role: 'patient' satisfies UserRole }, { status: 201 }) }),
  http.get('/api/v1/auth/me', ({ request }) => response(users[roleOf(request)])),
  http.get('/api/v1/auth/admin/users/', () => response(Object.values(users).map((user) => ({ ...user, isActive: true })))),
  http.get('/api/v1/auth/admin/doctors/', () => response(adminDoctors)),
  http.post('/api/v1/auth/admin/doctors/', async ({ request }) => {
    const body = await request.json() as { email: string; firstName: string; lastName: string; licenseNumber: string; biography?: string }
    const doctor = { id: crypto.randomUUID(), email: body.email, firstName: body.firstName, lastName: body.lastName, licenseNumber: body.licenseNumber, biography: body.biography ?? '', isActive: true, defaultAppointmentMinutes: 30 }
    adminDoctors = [...adminDoctors, doctor]
    return response(doctor, { status: 201 })
  }),
  http.get('/api/v1/specialties', () => response(specialties)),
  http.get('/api/v1/clinics', () => response(clinics)),
  http.get('/api/v1/doctors', ({ request }) => { const url = new URL(request.url); const specialtyId = url.searchParams.get('specialtyId'); const clinicId = url.searchParams.get('clinicId'); return response(doctors.filter((doctor) => (!specialtyId || doctor.specialtyIds.includes(specialtyId)) && (!clinicId || doctor.clinicIds.includes(clinicId)))) }),
  http.get('/api/v1/availability', () => response([8, 9, 10, 11, 12, 15, 16, 17].map((hour) => ({ id: `slot-${hour}`, startsAt: inDays(5, hour), endsAt: inDays(5, hour + 1), available: hour !== 10 })))),
  http.get('/api/v1/appointments', ({ request }) => { const role = roleOf(request); return response(role === 'doctor' ? appointments.filter((item) => item.doctorId === 'doctor-1') : appointments) }),
  http.post('/api/v1/appointments', async ({ request }) => { const body = await request.json() as { specialtyId: string; doctorId: string; clinicId: string; slotId: string; reason?: string }; if (body.slotId === 'slot-10') return response({ message: 'Ese horario acaba de ser reservado. Elige otra opción.' }, { status: 409 }); const doctor = doctors.find((item) => item.id === body.doctorId)!; const specialty = specialties.find((item) => item.id === body.specialtyId)!; const clinic = clinics.find((item) => item.id === body.clinicId)!; const hour = Number(body.slotId.replace('slot-', '')); const appointment: Appointment = { id: crypto.randomUUID(), patientName: 'Ana López', doctorName: doctor.name, doctorId: doctor.id, specialty: specialty.name, clinic: clinic.name, startsAt: inDays(5, hour), endsAt: inDays(5, hour + 1), status: 'confirmed', reason: body.reason }; appointments = [appointment, ...appointments]; return response(appointment, { status: 201 }) }),
  http.patch('/api/v1/appointments/:id', async ({ request, params }) => { const body = await request.json() as { action: 'cancel' | 'complete' }; const index = appointments.findIndex((item) => item.id === params.id); if (index < 0) return response({ message: 'Cita no encontrada.' }, { status: 404 }); const status: AppointmentStatus = body.action === 'cancel' ? 'cancelled' : 'completed'; appointments[index] = { ...appointments[index], status }; return response(appointments[index]) }),
  http.post('/api/v1/appointments/:id/reschedule', async ({ request, params }) => {
    const body = await request.json() as { specialtyId: string; doctorId: string; clinicId: string; slotId: string; reason?: string }
    const index = appointments.findIndex((item) => item.id === params.id)
    const doctor = doctors.find((item) => item.id === body.doctorId)
    const specialty = specialties.find((item) => item.id === body.specialtyId)
    const clinic = clinics.find((item) => item.id === body.clinicId)
    if (index < 0 || !doctor || !specialty || !clinic) return response({ message: 'No se pudo reprogramar la cita.' }, { status: 404 })
    if (body.slotId === 'slot-10') return response({ message: 'Ese horario acaba de ser reservado. Elige otra opción.' }, { status: 409 })
    const hour = Number(body.slotId.replace('slot-', ''))
    const replacement: Appointment = { id: crypto.randomUUID(), patientName: 'Ana López', doctorName: doctor.name, doctorId: doctor.id, specialty: specialty.name, clinic: clinic.name, startsAt: inDays(5, hour), endsAt: inDays(5, hour + 1), status: 'confirmed', reason: body.reason }
    appointments[index] = { ...appointments[index], status: 'rescheduled' }
    appointments = [replacement, ...appointments]
    return response(replacement, { status: 201 })
  }),
  http.post('/api/v1/consultations', async ({ request }) => {
    const body = await request.json() as { appointmentId: string; clinicalSummary: string }
    const index = appointments.findIndex((item) => item.id === body.appointmentId)
    if (index < 0 || appointments[index].status !== 'confirmed') return response({ message: 'Solo se puede registrar una consulta para una cita confirmada.' }, { status: 400 })
    appointments[index] = { ...appointments[index], status: 'completed' }
    return response({ id: crypto.randomUUID(), ...body }, { status: 201 })
  }),
]
