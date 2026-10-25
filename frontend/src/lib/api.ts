import type { AdminDoctor, AdminUser, Appointment, AvailabilitySlot, CatalogRecord, Clinic, Consultation, CreateAppointmentInput, CreateDoctorInput, Doctor, NotificationFeed, PatientProfile, Specialty, User } from '../types/api'

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

async function refreshSession() {
  await ensureCsrf()
  const response = await fetch(`${baseUrl}/auth/refresh`, {
    method: 'POST', credentials: 'include', headers: csrfToken ? { 'X-CSRFToken': csrfToken } : {},
  })
  return response.ok
}

async function request<T>(path: string, init: RequestInit = {}, retried = false): Promise<T> {
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
  if (response.status === 401 && !useMocks && !retried && path !== '/auth/refresh' && await refreshSession()) {
    return request<T>(path, init, true)
  }
  if (!response.ok) {
    const body = await response.json().catch(() => ({ message: 'No se pudo completar la solicitud.' })) as { message?: string; detail?: string }
    throw new Error(body.message ?? body.detail ?? 'No se pudo completar la solicitud.')
  }
  return response.status === 204 ? undefined as T : response.json() as Promise<T>
}

export const api = {
  login: (email: string, password: string) => request<User>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  register: (name: string, email: string, password: string) => request<User>('/auth/register', { method: 'POST', body: JSON.stringify({ name, email, password }) }),
  logout: () => request<void>('/auth/logout', { method: 'POST' }),
  me: () => request<User>('/auth/me'),
  refresh: () => request<void>('/auth/refresh', { method: 'POST' }),
  specialties: () => request<Specialty[]>('/specialties'),
  clinics: () => request<Clinic[]>('/clinics'),
  doctors: (specialtyId?: string, clinicId?: string) => request<Doctor[]>(`/doctors?specialtyId=${specialtyId ?? ''}&clinicId=${clinicId ?? ''}`),
  availability: (doctorId: string, clinicId: string) => request<AvailabilitySlot[]>(`/availability?doctorId=${doctorId}&clinicId=${clinicId}`),
  appointments: (filters: { date?: string; from?: string; to?: string; status?: string } = {}) => request<Appointment[]>(`/appointments${Object.keys(filters).length ? `?${new URLSearchParams(Object.entries(filters).filter(([, value]) => value) as [string, string][]).toString()}` : ''}`),
  createAppointment: (input: CreateAppointmentInput) => request<Appointment>('/appointments', { method: 'POST', body: JSON.stringify(input) }),
  updateAppointment: (id: string, action: 'cancel' | 'complete' | 'no_show', reason = '') => request<Appointment>(`/appointments/${id}`, { method: 'PATCH', body: JSON.stringify({ action, reason }) }),
  rescheduleAppointment: (id: string, input: CreateAppointmentInput) => request<Appointment>(`/appointments/${id}/reschedule`, { method: 'POST', body: JSON.stringify(input) }),
  createConsultation: (input: Consultation) => request<Consultation>('/consultations', { method: 'POST', body: JSON.stringify(input) }),
  adminUsers: () => request<AdminUser[]>('/auth/admin/users/'),
  updateAdminUser: (id: string, input: Partial<Pick<AdminUser, 'isActive'>>) => request<AdminUser>(`/auth/admin/users/${id}/`, { method: 'PATCH', body: JSON.stringify(input) }),
  adminDoctors: () => request<AdminDoctor[]>('/auth/admin/doctors/'),
  createDoctor: (input: CreateDoctorInput) => request<AdminDoctor>('/auth/admin/doctors/', { method: 'POST', body: JSON.stringify(input) }),
  patientProfile: () => request<PatientProfile>('/auth/profile'),
  updatePatientProfile: (input: Partial<PatientProfile>) => request<PatientProfile>('/auth/profile', { method: 'PATCH', body: JSON.stringify(input) }),
  notifications: () => request<NotificationFeed>('/notifications'),
  markNotificationRead: (id: string) => request<void>(`/notifications/${id}/read`, { method: 'PATCH' }),
  markAllNotificationsRead: () => request<void>('/notifications/read-all', { method: 'PATCH' }),
  adminCatalog: <T extends CatalogRecord>(resource: string) => request<T[]>(`/admin/catalogs/${resource}/`),
  createAdminCatalog: <T extends CatalogRecord>(resource: string, input: Record<string, unknown>) => request<T>(`/admin/catalogs/${resource}/`, { method: 'POST', body: JSON.stringify(input) }),
  updateAdminCatalog: <T extends CatalogRecord>(resource: string, id: string, input: Record<string, unknown>) => request<T>(`/admin/catalogs/${resource}/${id}/`, { method: 'PATCH', body: JSON.stringify(input) }),
}
