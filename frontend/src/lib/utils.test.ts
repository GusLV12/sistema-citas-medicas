import { describe, expect, it } from 'vitest'
import { canPatientChange } from './utils'

describe('regla de modificación de cita', () => {
  it('permite al paciente modificar una cita con más de 24 horas', () => expect(canPatientChange(new Date(Date.now() + 25 * 60 * 60 * 1000).toISOString())).toBe(true))
  it('bloquea cambios cuando faltan menos de 24 horas', () => expect(canPatientChange(new Date(Date.now() + 23 * 60 * 60 * 1000).toISOString())).toBe(false))
})
