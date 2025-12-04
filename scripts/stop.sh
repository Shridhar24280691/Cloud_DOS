#!/bin/bash
echo "Stopping existing application processes..."

# Stop Django dev server (if running)
pkill -f "manage.py runserver" || true

# Stop gunicorn (if running)
pkill -f "gunicorn" || true
pkill -f "wsgi:application" || true

echo "Stop script completed."
exit 0
