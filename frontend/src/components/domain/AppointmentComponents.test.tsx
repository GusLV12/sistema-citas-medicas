import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { AppointmentStatusBadge, SlotButton } from './AppointmentComponents'

describe('componentes de citas', () => {
  it('expresa el estado de una cita con texto', () => { render(<AppointmentStatusBadge status="confirmed" />); expect(screen.getByText('Confirmada')).toBeInTheDocument() })
  it('deshabilita un horario ocupado', () => { render(<SlotButton selected={false} onSelect={() => undefined} slot={{ id: 'a', startsAt: '2030-01-01T10:00:00Z', endsAt: '2030-01-01T11:00:00Z', available: false }} />); expect(screen.getByRole('button')).toBeDisabled() })
})
