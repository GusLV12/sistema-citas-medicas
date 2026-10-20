import type { Appointment, AvailabilitySlot, Clinic, Consultation, CreateAppointmentInput, Doctor, Specialty, User } from '../types/api'

const baseUrl = import.meta.env.VITE_API_URL ?? '/api/v1'
export const useMocks = import.meta.env.VITE_USE_MOCKS !== 'false'
let csrfToken: string | undefined

function cookie(name: string) {
  return document.cookie.split('; ').find((item) => item.startsWith(`${name}=`))?.split('=')[1]
}

async function ensureCsrf() {
  if (useMocks || csrfToken) return
  const response = await fetch(`${baseUrl}/auth/csrf`, { credentials: 'include' })
  const body = await response.json() as { csrfToken: string }
  csrfToken = body.csrfToken ?? cookie('csrftoken')
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const unsafe = !['GET', 'HEAD', 'OPTIONS'].includes(init.method ?? 'GET')
  if (unsafe) await ensureCsrf()
  const role = useMocks ? sessionStorage.getItem('demo-role') : null
  const response = await fetch(`${baseUrl}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
      ...(role ? { 'X-Demo-Role': role } : {}),
      ...init.headers,
    },
    ...init,
  })
  if (!response.ok) {
    const body = await response.json().catch(() => ({ message: 'No se pudo completar la solicitud.' })) as { message?: string }
    throw new Error(body.message ?? 'No se pudo completar la solicitud.')
  }
  return response.status === 204 ? undefined as T : response.json() as Promise<T>
}

export const api = {
  login: (email: string, password: string) => request<User>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  register: (name: string, email: string, password: string) => request<User>('/auth/register', { method: 'POST', body: JSON.stringify({ name, email, password }) }),
  logout: () => request<void>('/auth/logout', { method: 'POST' }),
  me: () => request<User>('/auth/me'),
  specialties: () => request<Specialty[]>('/specialties'),
  clinics: () => request<Clinic[]>('/clinics'),
  doctors: (specialtyId?: string, clinicId?: string) => request<Doctor[]>(`/doctors?specialtyId=${specialtyId ?? ''}&clinicId=${clinicId ?? ''}`),
  availability: (doctorId: string, clinicId: string) => request<AvailabilitySlot[]>(`/availability?doctorId=${doctorId}&clinicId=${clinicId}`),
  appointments: () => request<Appointment[]>('/appointments'),
  createAppointment: (input: CreateAppointmentInput) => request<Appointment>('/appointments', { method: 'POST', body: JSON.stringify(input) }),
  updateAppointment: (id: string, action: 'cancel' | 'complete') => request<Appointment>(`/appointments/${id}`, { method: 'PATCH', body: JSON.stringify({ action }) }),
  rescheduleAppointment: (id: string, input: CreateAppointmentInput) => request<Appointment>(`/appointments/${id}/reschedule`, { method: 'POST', body: JSON.stringify(input) }),
  createConsultation: (input: Consultation) => request<Consultation>('/consultations', { method: 'POST', body: JSON.stringify(input) }),
}
