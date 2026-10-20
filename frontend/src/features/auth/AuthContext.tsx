import { useMemo, useState, type ReactNode } from 'react'
import { api, useMocks } from '../../lib/api'
import type { User, UserRole } from '../../types/api'
import { AuthContext, type AuthValue } from './auth-context'

const demoUsers: Record<UserRole, User> = { patient: { id: 'patient-1', name: 'Ana López', email: 'paciente@salud.mx', role: 'patient' }, doctor: { id: 'doctor-1', name: 'Dra. Sofía Ramos', email: 'medico@salud.mx', role: 'doctor' }, admin: { id: 'admin-1', name: 'Mariana Cruz', email: 'admin@salud.mx', role: 'admin' } }
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => { const raw = sessionStorage.getItem('demo-user'); return raw ? JSON.parse(raw) as User : null })
  const store = (next: User) => { sessionStorage.setItem('demo-user', JSON.stringify(next)); sessionStorage.setItem('demo-role', next.role); setUser(next); return next }
  const value = useMemo<AuthValue>(() => ({ user, login: async (email, password) => store(await api.login(email, password)), register: async (name, email, password) => store(await api.register(name, email, password)), logout: async () => { try { if (!useMocks) await api.logout() } finally { sessionStorage.clear(); setUser(null) } }, setDemoRole: (role) => store(demoUsers[role]) }), [user])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
