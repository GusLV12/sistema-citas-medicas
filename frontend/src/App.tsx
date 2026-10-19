import { Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout, RequireRole } from './components/layout/AppLayout'
import { AdminCatalogPage } from './features/admin/AdminCatalogPage'
import { AuthPage } from './features/auth/AuthPage'
import { AppointmentBookingPage } from './features/appointments/AppointmentBookingPage'
import { AppointmentDetailPage } from './features/appointments/AppointmentDetailPage'
import { AppointmentsPage } from './features/appointments/AppointmentsPage'
import { PatientDashboardPage } from './features/appointments/PatientDashboardPage'
import { DoctorAgendaPage } from './features/doctor/DoctorAgendaPage'

export default function App() {
  return <Routes>
    <Route path="/login" element={<AuthPage mode="login" />} />
    <Route path="/registro" element={<AuthPage mode="register" />} />
    <Route element={<RequireRole />}><Route element={<AppLayout />}>
      <Route path="/paciente" element={<RequireRole roles={['patient']}><PatientDashboardPage /></RequireRole>} />
      <Route path="/paciente/reservar" element={<RequireRole roles={['patient']}><AppointmentBookingPage /></RequireRole>} />
      <Route path="/paciente/citas" element={<RequireRole roles={['patient']}><AppointmentsPage /></RequireRole>} />
      <Route path="/citas/:appointmentId" element={<AppointmentDetailPage />} />
      <Route path="/medico" element={<RequireRole roles={['doctor']}><DoctorAgendaPage /></RequireRole>} />
      <Route path="/administracion" element={<RequireRole roles={['admin']}><AdminCatalogPage /></RequireRole>} />
    </Route></Route>
    <Route path="*" element={<Navigate to="/paciente" replace />} />
  </Routes>
}
