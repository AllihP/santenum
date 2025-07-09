import os
import django

# Configure Django settings (important!)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'santenumerique.settings') # Remplacez 'santenumerique' par le nom de votre projet principal si c'est différent
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not username or not email or not password:
    print("Superuser environment variables are not set. Skipping superuser creation.")
else:
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser '{username}'...")
        User.objects.create_superuser(username, email, password)
        print("Superuser created successfully.")
    else:
        print(f"Superuser '{username}' already exists. Skipping creation.")
