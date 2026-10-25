import { Bell, CalendarPlus, CalendarRange, ClipboardList, LogOut, ShieldCheck, Stethoscope, UserRound } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import type { ReactNode } from 'react'
import { Link, Navigate, NavLink, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../../features/auth/useAuth'
import { useMocks } from '../../lib/api'
import { api } from '../../lib/api'
import type { UserRole } from '../../types/api'
import { Button } from '../ui'

export function RequireRole({ roles, children }: { roles?: UserRole[]; children?: ReactNode }) { const { user, isRestoring } = useAuth(); const location = useLocation(); if (isRestoring) return <main className="p-6">Restaurando sesión…</main>; if (!user) return <Navigate to="/login" state={{ from: location }} replace />; if (roles && !roles.includes(user.role)) return <Navigate to={user.role === 'patient' ? '/paciente' : user.role === 'doctor' ? '/medico' : '/administracion'} replace />; return children ?? <Outlet /> }
const navigation: Record<UserRole, { to: string; label: string; icon: typeof CalendarRange }[]> = { patient: [{ to: '/paciente', label: 'Inicio', icon: CalendarRange }, { to: '/paciente/reservar', label: 'Reservar cita', icon: CalendarPlus }, { to: '/paciente/citas', label: 'Mis citas', icon: ClipboardList }, { to: '/paciente/perfil', label: 'Mi perfil', icon: UserRound }], doctor: [{ to: '/medico', label: 'Mi agenda', icon: Stethoscope }], admin: [{ to: '/administracion', label: 'Administración', icon: ShieldCheck }] }
export function AppLayout() {
  const { user, logout, setDemoRole } = useAuth()
  const notifications = useQuery({ queryKey: ['notifications'], queryFn: api.notifications, enabled: Boolean(user) })
  if (!user) return null
  const unread = notifications.data?.unreadCount ?? 0
  return <div className="min-h-screen"><a className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-white focus:p-3 focus:text-primary" href="#main-content">Saltar al contenido</a><header className="border-b border-line bg-white"><div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4"><Link to="/" className="font-heading font-extrabold text-primary">Salud Agenda</Link><div className="flex items-center gap-3">{useMocks && <select aria-label="Rol de demostración" value={user.role} onChange={(event) => setDemoRole(event.target.value as UserRole)} className="rounded border border-line bg-white p-2 text-sm"><option value="patient">Paciente</option><option value="doctor">Médico</option><option value="admin">Administración</option></select>}<Link aria-label={`Notificaciones${unread ? `, ${unread} sin leer` : ''}`} className="relative rounded p-2 text-primary hover:bg-teal-50" to="/notificaciones"><Bell size={20} />{unread > 0 && <span className="absolute -right-1 -top-1 min-w-5 rounded-full bg-danger px-1 text-center text-xs font-bold text-white">{unread > 9 ? '9+' : unread}</span>}</Link><Button variant="ghost" onClick={() => { void logout() }}><LogOut size={17} />Salir</Button></div></div></header><div className="mx-auto grid max-w-6xl gap-6 px-6 py-6 md:grid-cols-[13rem_1fr]"><aside aria-label="Navegación principal" className="flex gap-2 overflow-x-auto md:flex-col">{navigation[user.role].map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} className={({ isActive }) => `flex min-h-11 items-center gap-2 rounded-md px-3 text-sm font-semibold ${isActive ? 'bg-teal-100 text-primary' : 'text-muted hover:bg-white'}`}><Icon size={18} />{label}</NavLink>)}</aside><main id="main-content" tabIndex={-1}><Outlet /></main></div></div>
}
