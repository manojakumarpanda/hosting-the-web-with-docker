#!/bin/bash
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py makemigrations usermanagement
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py makemigrations organization
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py makemigrations project
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py makemigrations operation
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py migrate usermanagement
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py migrate organization
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py migrate project
/home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py migrate operation
# /home/ubuntu/django/mmtxt/bin/python /home/ubuntu/django/crm/manage.py migrate django_celery_beat
chmod 777 -R /home/ubuntu/django/crm
mkdir -p /home/ubuntu/django/media_files
chmod 777 /home/ubuntu/django/media_files
service supervisor start
apache2ctl -D FOREGROUND