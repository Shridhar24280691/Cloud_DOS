#!/bin/bash
echo "Stopping existing application processes..."

pkill -f "manage.py runserver" || true
pkill -f "gunicorn" || true
pkill -f "wsgi:application" || true

echo "Stop script completed."
exit 0
