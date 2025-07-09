from pathlib import Path
import os
import dj_database_url
import sys
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# --- Configuration de base du projet ---

# Détermine le chemin de base de votre projet.
# Si settings.py est dans 'santenumerique/', BASE_DIR sera le répertoire parent de 'santenumerique/'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge les variables d'environnement depuis le fichier .env
# Assurez-vous que .env est à la racine de votre projet (un niveau au-dessus du dossier santenumerique qui contient settings.py).
load_dotenv(os.path.join(BASE_DIR, '.env')) # Chemin corrigé pour .env

# --- Paramètres de sécurité et de débogage ---

# SECRET_KEY: Clé secrète utilisée par Django. NE DOIT JAMAIS ÊTRE EXPOSÉE EN PRODUCTION.
# Utilisez une variable d'environnement 'DJANGO_SECRET_KEY'.
# La valeur par défaut ne doit être utilisée qu'en développement.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'Am-mi/1324576890#')

# DEBUG: Active/désactive le mode débogage de Django. DOIT ÊTRE FALSE EN PRODUCTION.
# Utilisé pour basculer entre développement et production.
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true' # Utilise .lower() pour une meilleure robustesse

# ALLOWED_HOSTS: Liste des noms de domaine que cette installation Django peut servir.
# Crucial pour la sécurité en production.
ALLOWED_HOSTS = []

# En mode débogage, autorise l'accès local.
if DEBUG:
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('santenumerique.onrender.com')
else:
    # En production, récupère les hôtes autorisés depuis 'DJANGO_ALLOWED_HOSTS'.
    # Les domaines doivent être séparés par des virgules, ex: "example.com,www.example.com"
    allowed_hosts_env = os.getenv('DJANGO_ALLOWED_HOSTS')
    if allowed_hosts_env:
        ALLOWED_HOSTS.extend([h.strip() for h in allowed_hosts_env.split(',') if h.strip()])

    # Ajoute l'hostname externe de Render si disponible.
    render_external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_external_hostname and render_external_hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_external_hostname)

# --- Définition des applications ---

INSTALLED_APPS = [
    # Applications intégrées de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Nécessaire pour servir les fichiers statiques

    # Vos applications
    'webapp',
    'events',
    'candidature',
    'elearning',
]

# --- Middlewares ---

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Pour servir les fichiers statiques en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Pour la gestion des langues
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URL Configuration ---

ROOT_URLCONF = 'santenumerique.urls'

# --- Configuration des Templates ---

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS: Liste des répertoires où Django cherchera des templates en plus des répertoires d'applications.
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Chemin corrigé
        'APP_DIRS': True, # Permet à Django de chercher des templates dans les dossiers 'templates/' de chaque app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- WSGI & ASGI Applications ---

WSGI_APPLICATION = 'santenumerique.wsgi.application'
ASGI_APPLICATION = 'santenumerique.asgi.application' # Si vous utilisez ASGI (pour websockets par exemple)

# --- Modèle utilisateur personnalisé ---

AUTH_USER_MODEL = 'elearning.Utilisateur'

# --- Configuration de la Base de Données ---

# Utilise DATABASE_URL pour la production (Render, Heroku, etc.)
# Fallback sur SQLite pour le développement local si DATABASE_URL n'est pas défini.
DATABASE_URL = os.environ.get('postgresql://hillaprince:n5xjsgXwJ46GYDqIJveV8AH4eoNoWyXI@dpg-d1g0io3ipnbc73a5cjdg-a.oregon-postgres.render.com/santenumerique')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    # dj_database_url.parse détecte l'engine, pas besoin de le forcer.
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # Chemin corrigé
        }
    }

# --- Validation des mots de passe ---

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --- Internationalisation et Localisation (I18N & L10N) ---

# Définition de la langue par défaut du site.
LANGUAGE_CODE = 'fr'

# Liste des langues supportées par votre application.
# La fonction _() est utilisée pour marquer les chaînes comme traduisibles.
LANGUAGES = [
    ('fr', _('French')),
    ('en', _('English')),
    ('ar', _('Arabic')),
]

# Fuseau horaire du site.
TIME_ZONE = 'Africa/Ndjamena'

USE_I18N = True # Active le système de traduction de Django
USE_TZ = True   # Active le support des fuseaux horaires (recommandé)

# --- Fichiers Statiques (CSS, JS, Images) et Fichiers Média (Uploads Utilisateurs) ---

# STATIC_URL: URL de base pour les fichiers statiques.
STATIC_URL = '/static/'
# In santenumerique/settings.py

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # This is where collectstatic will put files

STATICFILES_DIRS = [
    # Example 1: If 'styles.css' is in 'your_project_root/santenumerique/styles/styles.css'
    # This means your 'styles' folder is directly under your main project folder.
    os.path.join(BASE_DIR, 'santenumerique', 'styles'),

    # Example 2: If 'styles.css' is in 'your_project_root/santenumerique/static/styles/styles.css'
    # This means you have a 'static' folder directly under your main project folder.
    # os.path.join(BASE_DIR, 'santenumerique', 'static'),

    # Example 3: If 'styles.css' is in 'your_project_root/webapp/static/styles/styles.css'
    # (Where 'webapp' is one of your Django apps listed in INSTALLED_APPS)
    # In this case, you generally *don't* need to add webapp/static to STATICFILES_DIRS.
    # Django automatically finds 'static/' folders within INSTALLED_APPS.
    # However, if your reference is simply `{% static 'styles/styles.css' %}`
    # and it's only in `webapp/static/`, then Django *should* find it.
    # If it doesn't, it might mean your template path or your INSTALLED_APPS is off.
]

# Ensure this is correctly configured for production with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# STORAGES: Configuration des backends de stockage.
# "default" est pour les fichiers média.
# "staticfiles" est pour les fichiers statiques, en utilisant WhiteNoise pour la compression et le cache.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# MEDIA_URL: URL publique pour les fichiers médias uploadés par les utilisateurs.
MEDIA_URL = '/media/'

# MEDIA_ROOT: Chemin absolu où les fichiers médias uploadés seront stockés.
# Pour la production sur Render, il est fortement recommandé d'utiliser un stockage d'objets (S3, GCS)
# avec django-storages pour la persistance et la scalabilité.
# Si vous n'utilisez pas de stockage d'objets, sachez que les fichiers sur le système de fichiers de Render
# ne sont PAS persistants entre les déploiements ou les redémarrages d'instances.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Chemin par défaut pour le développement.
                                            # Changez ceci si vous utilisez un service de stockage cloud.

# --- Configuration du type de champ de clé primaire par défaut ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- URLs de connexion/déconnexion ---

LOGIN_URL = '/accounts/login/'        # Page de connexion personnalisée (si elle existe)
LOGIN_REDIRECT_URL = '/elearning/profile/' # Redirection après connexion réussie
LOGOUT_REDIRECT_URL = '/'             # Redirection après déconnexion

# --- Configuration spécifique pour les tests ---

# Ces paramètres sont activés lorsque la commande 'test' est exécutée.
if 'test' in sys.argv:
    # Utilise un backend email en mémoire pour éviter d'envoyer de vrais emails pendant les tests.
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    # Utilise un répertoire temporaire pour les fichiers média lors des tests.
    MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media_temp') # Chemin corrigé
    # Assurez-vous que ce répertoire est nettoyé après les tests si nécessaire.

# --- Configuration du Logging (Journalisation) ---

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose', # Utilisation d'un formatter défini ci-dessous
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'loggers': {
        '': { # Logger racine, capture tous les messages
            'handlers': ['console'],
            'level': 'INFO' if not DEBUG else 'DEBUG', # INFO en production, DEBUG en développement
            'propagate': True,
        },
        'django': { # Logger spécifique à Django
            'handlers': ['console'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': False, # Ne propage pas au logger racine pour éviter les doublons
        },
    },
}
