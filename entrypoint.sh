#!/usr/bin/env bash

echo "Applying database migrations..."
python manage.py migrate --noinput || { echo "Migrations failed!"; exit 1; } # Add error handling

echo "Running create_superuser.py script..."
python create_superuser.py || { echo "Superuser creation failed!"; exit 1; } # Add error handling

echo "Starting Gunicorn..."
gunicorn santenumerique.wsgi:application --bind 0.0.0.0:$PORT || { echo "Gunicorn failed to start!"; exit 1; } # Add error handling
