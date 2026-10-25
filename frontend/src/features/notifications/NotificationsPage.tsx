import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Button, Card, EmptyState } from '../../components/ui'
import { api } from '../../lib/api'
import { formatDateTime } from '../../lib/utils'

export function NotificationsPage() {
  const queryClient = useQueryClient()
  const feed = useQuery({ queryKey: ['notifications'], queryFn: api.notifications })
  const markRead = useMutation({ mutationFn: api.markNotificationRead, onSuccess: () => queryClient.invalidateQueries({ queryKey: ['notifications'] }) })
  const markAll = useMutation({ mutationFn: api.markAllNotificationsRead, onSuccess: () => queryClient.invalidateQueries({ queryKey: ['notifications'] }) })
  if (feed.isLoading) return <p className="text-muted">Cargando notificaciones…</p>
  if (feed.isError) return <EmptyState title="No pudimos cargar tus notificaciones" description="Actualiza la página para intentarlo de nuevo." />
  const notifications = feed.data?.results ?? []
  return <div><header className="flex flex-wrap items-end justify-between gap-3"><div><p className="font-semibold text-primary">Comunicación</p><h1 className="font-heading text-3xl font-extrabold">Notificaciones</h1><p className="mt-2 text-muted">Avisos de tus citas y recordatorios dentro de Salud Agenda.</p></div>{feed.data?.unreadCount ? <Button variant="secondary" disabled={markAll.isPending} onClick={() => markAll.mutate()}>Marcar todas como leídas</Button> : null}</header><div className="mt-6 grid gap-3">{notifications.length ? notifications.map((notification) => <Card key={notification.id} className={notification.readAt ? 'opacity-75' : 'border-primary/30'}><div className="flex flex-wrap items-start justify-between gap-3"><div><p className="font-semibold">{notification.title}</p><p className="mt-1 text-sm text-muted">{notification.body}</p><p className="mt-2 text-xs text-muted">{formatDateTime(notification.createdAt)}</p></div><div className="flex gap-2">{notification.appointmentId && <Link className="min-h-11 px-2 py-2 text-sm font-semibold text-primary underline" to={`/citas/${notification.appointmentId}`}>Ver cita</Link>}{!notification.readAt && <Button variant="secondary" disabled={markRead.isPending} onClick={() => markRead.mutate(notification.id)}>Leída</Button>}</div></div></Card>) : <EmptyState title="No tienes notificaciones" description="Aquí aparecerán los cambios y recordatorios de tus citas." />}</div></div>
}
