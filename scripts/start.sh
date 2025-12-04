#!/bin/bash
cd /home/ec2-user/car_app
nohup python3 manage.py runserver 0.0.0.0:8080 > server.log 2>&1 &
