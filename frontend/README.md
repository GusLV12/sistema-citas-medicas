# Frontend · Sistema de Citas Médicas

Aplicación React con TypeScript para pacientes, médicos y administración. Usa datos simulados con MSW; la capa `src/lib/api.ts` está preparada para reemplazar los mocks por Django REST Framework.

## Ejecutar

```powershell
npm install
npm run dev
```

Abre la URL indicada por Vite. Para la demostración, inicia sesión con `paciente@salud.mx`, `medico@salud.mx` o `admin@salud.mx`; cualquier contraseña de ocho caracteres funciona.

## Comandos

- `npm run build`: valida TypeScript y genera el paquete de producción.
- `npm test`: ejecuta pruebas unitarias e integración con MSW.
- `npm run lint`: revisa reglas estáticas con Oxlint.

## Integración con Django

Configura `VITE_API_URL` con la ruta de la API, por ejemplo `/api/v1`, y establece `VITE_USE_MOCKS=false`. Django debe exponer los contratos de `src/lib/api.ts`, usar JWT en cookies `HttpOnly` y validar permisos, disponibilidad y solapamientos en el servidor.
