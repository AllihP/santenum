#!/usr/bin/env bash
# entrypoint.sh

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn santenumerique.wsgi:application --bind 0.0.0.0:$PORT
