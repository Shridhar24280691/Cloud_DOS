#!/bin/bash
cd /home/ec2-user/car_app

# Ensure log file is writable
touch server.log
chmod 666 server.log
pkill -f "manage.py runserver" || true
# Start Django in background
nohup python3 manage.py runserver 0.0.0.0:8080 >> server.log 2>&1 &
exit 0
