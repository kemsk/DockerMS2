#!/bin/bash

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Start the application using Gunicorn
python -m gunicorn --bind 0.0.0.0:8003 --workers 3 XU_AD.wsgi:application