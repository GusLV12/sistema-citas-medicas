# Sistema de Citas Médicas

Aplicación web para pacientes, médicos y administración. El backend expone una API Django REST y el frontend React consume la API o datos simulados durante el desarrollo.

## Requisitos

- Docker Desktop, para PostgreSQL 16.
- Python 3.12 o compatible.
- Node.js LTS y npm.

## Inicio rápido

Ejecuta los siguientes comandos desde la raíz del repositorio en PowerShell.

### 1. Configura las variables de entorno

```powershell
Copy-Item .env.example .env
Copy-Item frontend/.env.example frontend/.env.local
```

Los valores de ejemplo son seguros únicamente para desarrollo local. No subas ninguno de estos archivos al repositorio.

### 2. Inicia PostgreSQL

```powershell
docker compose up -d db
docker compose ps
```

El contenedor escucha solamente en `127.0.0.1:5432`. Para detenerlo sin perder datos, usa `docker compose stop db`.

### 3. Prepara y ejecuta la API

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py seed_demo
.\.venv\Scripts\python manage.py runserver
```

La API queda disponible en `http://localhost:8000/api/v1/`. Mantén esta terminal abierta mientras uses el frontend integrado.

### 4. Prepara y ejecuta el frontend

En otra terminal, desde la raíz del repositorio:

```powershell
cd frontend
npm install
npm run dev
```

Abre la URL que indica Vite, normalmente `http://localhost:5173`.

`frontend/.env.local` se crea con `VITE_USE_MOCKS=false`, por lo que el frontend utiliza Django. Para trabajar sólo con datos simulados, cambia el valor a `true` o elimina el archivo `.env.local`.

## Cuentas de demostración

Después de ejecutar `seed_demo`, todas las cuentas usan la contraseña `demo1234`.

| Rol | Correo |
| --- | --- |
| Paciente | `paciente@salud.mx` |
| Médico | `medico@salud.mx` |
| Administración | `admin@salud.mx` |

## Validación

Con PostgreSQL iniciado, valida el backend:

```powershell
cd backend
.\.venv\Scripts\python -m pytest
```

Valida el frontend:

```powershell
cd frontend
npm run lint
npm test
npm run build
```

Las pruebas del backend se ejecutan contra PostgreSQL porque validan las restricciones de reserva y sus transacciones.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `backend/` | API Django: cuentas, catálogos, agenda y consultas. |
| `frontend/` | Cliente React + TypeScript. |
| `database/schema.sql` | Esquema de referencia de PostgreSQL. |
| `docs/arquitectura-citas-medicas.md` | Modelo de dominio y reglas de negocio. |
| `DESIGN.md` | Guía de estilo y accesibilidad de la interfaz. |
| `docker-compose.yml` | PostgreSQL para desarrollo local. |

## Documentación adicional

- [Arquitectura funcional](docs/arquitectura-citas-medicas.md)
- [Diseño de la interfaz](DESIGN.md)
- [Objetivos de servicio](docs/slo.md)
- [Guía de contribución y comandos](AGENTS.md)
