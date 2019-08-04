#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py customcreatesuperuser

# preload some static data
#python manage.py loadinitiallocations

python manage.py collectstatic --noinput

rm -f logs/*
rm -f *.pid
# python manage.py runserver 0.0.0.0:8000
#gunicorn configuration.wsgi -b 0.0.0.0:8000 --worker-class=gevent  --timeout=90 --graceful-timeout=30 --reload
#gunicorn configuration.wsgi -b 0.0.0.0:8000 --worker-class=gevent --timeout=3600 --reload
supervisord -c devops/server/supervisord.conf