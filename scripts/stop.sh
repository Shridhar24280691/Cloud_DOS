#!/bin/bash
pkill -f "manage.py" || true
echo "Stop step completed."
exit 0
