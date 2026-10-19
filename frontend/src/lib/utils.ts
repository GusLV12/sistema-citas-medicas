import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export const cn = (...values: ClassValue[]) => twMerge(clsx(values))

export const formatDateTime = (value: string) => new Intl.DateTimeFormat('es-MX', {
  dateStyle: 'medium', timeStyle: 'short', timeZone: 'America/Mexico_City',
}).format(new Date(value))

export const canPatientChange = (startsAt: string) => new Date(startsAt).getTime() - Date.now() >= 24 * 60 * 60 * 1000
