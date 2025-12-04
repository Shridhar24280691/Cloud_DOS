#!/bin/bash
yum install -y python3 python3-pip nginx
pip3 install --upgrade pip
pip3 install -r /var/www/car_app/requirements.txt
systemctl enable nginx
systemctl restart nginx
