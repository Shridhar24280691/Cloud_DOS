#!/bin/bash
pkill -f "manage.py" || true
pkill -f "gunicorn" || true
echo "Stop script completed."
exit 0
