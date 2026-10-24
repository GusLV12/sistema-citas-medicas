import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { api, useMocks } from '../../lib/api'
import type { User, UserRole } from '../../types/api'
import { AuthContext, type AuthValue } from './auth-context'

const demoUsers: Record<UserRole, User> = { patient: { id: 'patient-1', name: 'Ana López', email: 'paciente@salud.mx', role: 'patient' }, doctor: { id: 'doctor-1', name: 'Dra. Sofía Ramos', email: 'medico@salud.mx', role: 'doctor' }, admin: { id: 'admin-1', name: 'Mariana Cruz', email: 'admin@salud.mx', role: 'admin' } }
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => { const raw = useMocks ? sessionStorage.getItem('demo-user') : null; return raw ? JSON.parse(raw) as User : null })
  const [isRestoring, setIsRestoring] = useState(!useMocks)
  const store = (next: User) => { if (useMocks) { sessionStorage.setItem('demo-user', JSON.stringify(next)); sessionStorage.setItem('demo-role', next.role) }; setUser(next); return next }
  useEffect(() => {
    if (useMocks) return
    let mounted = true
    api.me().then((next) => { if (mounted) store(next) }).catch(() => { if (mounted) setUser(null) }).finally(() => { if (mounted) setIsRestoring(false) })
    return () => { mounted = false }
  }, [])
  const value = useMemo<AuthValue>(() => ({ user, isRestoring, login: async (email, password) => store(await api.login(email, password)), register: async (name, email, password) => store(await api.register(name, email, password)), logout: async () => { try { if (!useMocks) await api.logout() } finally { sessionStorage.clear(); setUser(null) } }, setDemoRole: (role) => store(demoUsers[role]) }), [user, isRestoring])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
