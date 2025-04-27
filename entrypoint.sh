#!/usr/bin/env bash

# Collect static files and apply migrations
python manage.py collectstatic --noinput
python manage.py migrate --noinput

echo "⏳ Waiting for MySQL to be ready..."
python << END
import time
import socket
import os

host = os.environ.get("DATABASE_HOST", "db")
port = 3306
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        time.sleep(1)
END
echo "✅ Database is ready!"

# Collect static files and apply migrations
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create a superuser if not exists
echo "Checking if Django superuser exists..."
python -c "
import os
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print('Creating admin user...')
    User.objects.create_superuser('admin', 'admin@xuosa.com', os.getenv('DJANGO_SUPERUSER_PASSWORD', '1234'))
else:
    print('Admin user already exists.')
"

echo "Initialization completed."

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec python -m gunicorn --bind 0.0.0.0:8001 --workers 3 XUOSA_EVS.wsgi:application
