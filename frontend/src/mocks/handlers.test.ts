import { beforeEach, describe, expect, it } from 'vitest'
import { api } from '../lib/api'

describe('contrato simulado de citas', () => {
  beforeEach(() => sessionStorage.setItem('demo-role', 'patient'))

  it('crea y devuelve una cita de reemplazo de forma atómica', async () => {
    const replacement = await api.rescheduleAppointment('appointment-1', {
      specialtyId: 'cardiology', doctorId: 'doctor-1', clinicId: 'centro', slotId: 'slot-9', reason: 'Seguimiento',
    })
    const appointments = await api.appointments()
    expect(replacement.status).toBe('confirmed')
    expect(appointments.find((item) => item.id === 'appointment-1')?.status).toBe('rescheduled')
  })

  it('rechaza la reprogramación hacia un horario ocupado', async () => {
    await expect(api.rescheduleAppointment('appointment-2', {
      specialtyId: 'cardiology', doctorId: 'doctor-1', clinicId: 'centro', slotId: 'slot-10', reason: 'Seguimiento',
    })).rejects.toThrow('Ese horario acaba de ser reservado')
  })
})
