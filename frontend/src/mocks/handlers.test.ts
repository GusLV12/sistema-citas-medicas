import { beforeEach, describe, expect, it } from 'vitest'
import { api } from '../lib/api'

describe('contrato simulado de citas', () => {
  beforeEach(() => sessionStorage.setItem('demo-role', 'patient'))

  it('crea una cita de reemplazo y marca la original como reprogramada', async () => {
    const replacement = await api.createAppointment({
      specialtyId: 'cardiology', doctorId: 'doctor-1', clinicId: 'centro', slotId: 'slot-9', reason: 'Seguimiento',
    })
    const original = await api.rescheduleAppointment('appointment-1', replacement.id)
    expect(replacement.status).toBe('confirmed')
    expect(original.status).toBe('rescheduled')
  })
})
