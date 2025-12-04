#!/bin/bash
cd /home/ec2-user/car_app

# Kill old Django processes
pkill -f "manage.py"

# Start Django
nohup python3 manage.py runserver 0.0.0.0:8080 > server.log 2>&1 &
