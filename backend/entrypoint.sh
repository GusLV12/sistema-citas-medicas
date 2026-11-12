#!/bin/sh
set -eu

# A revision must not serve requests before its schema matches the application.
python manage.py migrate --noinput
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers 2 --timeout 60
