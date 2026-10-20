# Repository Guidelines

## Project Structure & Module Organization

- `database/schema.sql` is the PostgreSQL reference schema; `docs/images/` contains its diagram.
- `backend/` is the Django 5 API. Apps are grouped by domain: `accounts`, `catalogs`, `scheduling`, and `consultations`.
- `frontend/` is the React + TypeScript client. Reusable primitives live in `src/components/ui`, clinical components in `src/components/domain`, and route-specific behavior in `src/features`.
- `docs/` holds architecture and product documentation. Keep clinical data out of examples and screenshots.

## Build, Test, and Development Commands

Run these from the repository root unless stated otherwise:

- `docker compose up -d db` starts local PostgreSQL with its named persistent volume.
- `cd backend; .\\.venv\\Scripts\\python manage.py migrate` applies Django migrations.
- `cd backend; .\\.venv\\Scripts\\python -m pytest` runs backend tests against PostgreSQL.
- `cd backend; .\\.venv\\Scripts\\python manage.py runserver` starts the API at `localhost:8000`.
- `cd frontend; npm run dev` starts Vite. Copy `frontend/.env.example` to `.env.local` and set `VITE_USE_MOCKS=false` to use Django.
- `cd frontend; npm run lint`, `npm test`, and `npm run build` check frontend quality.

## Coding Style & Naming Conventions

Use four spaces in Python and two spaces in TypeScript, TSX, YAML, and CSS. Use `snake_case` for Python modules and functions, `PascalCase` for React components and Django models, and `camelCase` for TypeScript values and JSON API fields. Keep views thin: serializers validate HTTP input and scheduling services own transactional rules.

## Testing Guidelines

Add tests with each functional change. Test scheduling against PostgreSQL, never SQLite: booking conflicts, the 24-hour patient rule, permissions, atomic rescheduling, and the one-consultation rule are database behavior. Frontend tests use Vitest, Testing Library, and MSW; name them `*.test.ts` or `*.test.tsx`.

## Commit & Pull Request Guidelines

Use Conventional Commit prefixes, for example `feat(backend): add appointment availability` or `fix(frontend): clear session cookies on logout`. Keep SQL, backend, frontend, and documentation changes in focused commits. PRs should state the affected role or workflow, include validation commands, and attach screenshots for visible UI changes.

## Security & Configuration

Copy `.env.example` locally; never commit `.env`, credentials, JWTs, or patient data. PostgreSQL is bound to `127.0.0.1` for local use. Preserve cookie CSRF protection and database constraints when changing authentication or appointment flows.
