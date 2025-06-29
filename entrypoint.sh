#!/bin/bash

# Appliquer les migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Exécuter le script de création de super-utilisateur
echo "Running create_superuser.py script..."
python create_superuser.py

# Lancer Gunicorn
echo "Starting Gunicorn server..."
gunicorn santenumerique.wsgi:application --bind 0.0.0.0:$PORT
