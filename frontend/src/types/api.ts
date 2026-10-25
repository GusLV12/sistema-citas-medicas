export type UserRole = 'patient' | 'doctor' | 'admin'
export type AppointmentStatus = 'pending' | 'confirmed' | 'cancelled' | 'completed' | 'no_show' | 'rescheduled'

export interface User { id: string; name: string; email: string; role: UserRole }
export interface Specialty { id: string; name: string; description: string }
export interface Clinic { id: string; name: string; address: string }
export interface Doctor { id: string; name: string; specialtyIds: string[]; clinicIds: string[] }
export interface AvailabilitySlot { id: string; startsAt: string; endsAt: string; available: boolean }
export interface Appointment {
  id: string; patientName: string; doctorName: string; doctorId: string; specialty: string; clinic: string
  startsAt: string; endsAt: string; status: AppointmentStatus; reason?: string; cancellationReason?: string; canWriteConsultation?: boolean
}
export interface Consultation { appointmentId: string; clinicalSummary: string; followUpAt?: string }
export interface CreateAppointmentInput { specialtyId: string; doctorId: string; clinicId: string; slotId: string; reason?: string }
export interface AdminDoctor { id: string; email: string; firstName: string; lastName: string; licenseNumber: string; biography?: string; isActive: boolean; defaultAppointmentMinutes: number }
export interface CreateDoctorInput { email: string; password: string; firstName: string; lastName: string; licenseNumber: string; biography?: string }
export interface AdminUser extends User { isActive: boolean }
export interface PatientProfile { firstName: string; lastName: string; phone: string; birthDate?: string | null; emergencyContactName: string; emergencyContactPhone: string }
export interface Notification { id: string; appointmentId: string | null; kind: string; title: string; body: string; readAt: string | null; createdAt: string }
export interface NotificationFeed { results: Notification[]; unreadCount: number }
export type CatalogRecord = Record<string, unknown> & { id: string; is_active?: boolean; isActive?: boolean }
