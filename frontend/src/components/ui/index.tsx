import * as DialogPrimitive from '@radix-ui/react-dialog'
import { AlertCircle, X } from 'lucide-react'
import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode, SelectHTMLAttributes } from 'react'
import { cn } from '../../lib/utils'

export function Button({ className, variant = 'primary', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'danger' | 'ghost' }) {
  const styles = { primary: 'bg-primary text-white hover:bg-primary-hover', secondary: 'border border-line bg-surface text-ink hover:bg-slate-50', danger: 'bg-danger text-white hover:bg-red-800', ghost: 'text-primary hover:bg-teal-50' }
  return <button className={cn('inline-flex min-h-11 items-center justify-center gap-2 rounded-md px-4 py-2 font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-55', styles[variant], className)} {...props} />
}
export function Card({ children, className }: { children: ReactNode; className?: string }) { return <section className={cn('rounded-lg border border-line bg-surface p-5 shadow-sm', className)}>{children}</section> }
export function Field({ label, error, hint, children }: { label: string; error?: string; hint?: string; children: ReactNode }) {
  return <label className="grid gap-1.5 text-sm font-semibold text-ink"><span>{label}</span>{children}{hint && <span className="font-normal text-muted">{hint}</span>}{error && <span className="flex items-center gap-1 font-normal text-danger"><AlertCircle size={15} />{error}</span>}</label>
}
export function Input(props: InputHTMLAttributes<HTMLInputElement>) { return <input className={cn('min-h-11 rounded-md border border-line bg-white px-3 text-ink placeholder:text-slate-400', props.className)} {...props} /> }
export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) { return <select className={cn('min-h-11 rounded-md border border-line bg-white px-3 text-ink', props.className)} {...props} /> }
export function EmptyState({ title, description, action }: { title: string; description: string; action?: ReactNode }) { return <Card className="grid place-items-center gap-3 py-10 text-center"><h2 className="font-heading text-lg font-bold">{title}</h2><p className="max-w-md text-muted">{description}</p>{action}</Card> }
export function Dialog({ title, description, trigger, children }: { title: string; description: string; trigger: ReactNode; children: ReactNode }) {
  return <DialogPrimitive.Root><DialogPrimitive.Trigger asChild>{trigger}</DialogPrimitive.Trigger><DialogPrimitive.Portal><DialogPrimitive.Overlay className="fixed inset-0 bg-slate-950/35" /><DialogPrimitive.Content className="fixed left-1/2 top-1/2 w-[min(92vw,30rem)] -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white p-6 shadow-xl"><DialogPrimitive.Close className="absolute right-4 top-4 rounded p-1 text-muted" aria-label="Cerrar"><X size={20} /></DialogPrimitive.Close><DialogPrimitive.Title className="font-heading text-xl font-bold">{title}</DialogPrimitive.Title><DialogPrimitive.Description className="mt-2 text-muted">{description}</DialogPrimitive.Description><div className="mt-6">{children}</div></DialogPrimitive.Content></DialogPrimitive.Portal></DialogPrimitive.Root>
}
export function DialogClose({ children }: { children: ReactNode }) { return <DialogPrimitive.Close asChild>{children}</DialogPrimitive.Close> }
