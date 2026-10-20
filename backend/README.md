# Backend Django

## Inicio local

1. Copia `.env.example` a `.env` en la raíz y configura los valores.
2. Inicia PostgreSQL: `docker compose up -d db`.
3. Crea el entorno: `py -3.12 -m venv .venv`.
4. Instala dependencias: `.\.venv\Scripts\python -m pip install -r requirements.txt`.
5. Aplica la base: `.\.venv\Scripts\python manage.py migrate`.
6. Carga una demostración: `.\.venv\Scripts\python manage.py seed_demo`.
7. Ejecuta la API: `.\.venv\Scripts\python manage.py runserver`.

La API queda en `http://localhost:8000/api/v1`. Para integrar React, añade `VITE_USE_MOCKS=false` en `frontend/.env.local`.

## Pruebas

Con PostgreSQL iniciado, ejecuta `.\.venv\Scripts\python -m pytest`. Las pruebas no usan SQLite porque validan restricciones específicas de PostgreSQL.
