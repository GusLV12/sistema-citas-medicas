import { createContext } from 'react'
import type { User, UserRole } from '../../types/api'

export type AuthValue = {
  user: User | null
  login: (email: string, password: string) => Promise<User>
  register: (name: string, email: string, password: string) => Promise<User>
  logout: () => Promise<void>
  setDemoRole: (role: UserRole) => void
}

export const AuthContext = createContext<AuthValue | undefined>(undefined)
