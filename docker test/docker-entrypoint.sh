#!/bin/bash
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/seethos/manage.py makemigrations usermanagement
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/seethos/manage.py makemigrations uimanagement
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/seethos/manage.py migrate usermanagement
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/seethos/manage.py migrate uimanagement
chmod 777 -R /home/ubuntu/django/seethos
mkdir -p /home/ubuntu/django/media_files
chmod 777 /home/ubuntu/django/media_files
apache2ctl -D FOREGROUND