#!/bin/bash

# Attendre que la base de données soit prête (optionnel mais recommandé)
# if [ "$DATABASE_URL" ]; then
#   echo "Waiting for database to be ready..."
#   /usr/bin/wait-for-it $DATABASE_URL --timeout=30 --strict -- echo "Database is ready!"
# fi

# Appliquer les migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Créer le super-utilisateur si les variables d'environnement sont définies et si l'utilisateur n'existe pas
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser (if not exists)..."
    python -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); \
    if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists(): \
        User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_USERNAME'), os.environ.get('DJANGO_SUPERUSER_EMAIL'), os.environ.get('DJANGO_SUPERUSER_PASSWORD'))"
else
    echo "Superuser environment variables not set. Skipping superuser creation."
fi

# Lancer Gunicorn
echo "Starting Gunicorn server..."
gunicorn santenumerique.wsgi:application --bind 0.0.0.0:$PORT
