export type UserRole = 'patient' | 'doctor' | 'admin'
export type AppointmentStatus = 'pending' | 'confirmed' | 'cancelled' | 'completed' | 'no_show' | 'rescheduled'

export interface User { id: string; name: string; email: string; role: UserRole }
export interface Specialty { id: string; name: string; description: string }
export interface Clinic { id: string; name: string; address: string }
export interface Doctor { id: string; name: string; specialtyIds: string[]; clinicIds: string[] }
export interface AvailabilitySlot { id: string; startsAt: string; endsAt: string; available: boolean }
export interface Appointment {
  id: string; patientName: string; doctorName: string; doctorId: string; specialty: string; clinic: string
  startsAt: string; endsAt: string; status: AppointmentStatus; reason?: string; canWriteConsultation?: boolean
}
export interface Consultation { appointmentId: string; clinicalSummary: string; followUpAt?: string }
export interface CreateAppointmentInput { specialtyId: string; doctorId: string; clinicId: string; slotId: string; reason?: string }
