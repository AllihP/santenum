from pathlib import Path
import os
import dj_database_url
import sys
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables
load_dotenv(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# --- AJOUTEZ CES LIGNES POUR LE DÉBOGAGE ---
#print(f"DEBUG: DJANGO_DB_USER={os.getenv('DJANGO_DB_USER')}")
#print(f"DEBUG: DJANGO_DB_PASSWORD={os.getenv('DJANGO_DB_PASSWORD')}")
#print(f"DEBUG: DJANGO_DB_HOST={os.getenv('DJANGO_DB_HOST')}")
#print(f"DEBUG: DJANGO_DB_NAME={os.getenv('DJANGO_DB_NAME')}")
# ------------------------------------------




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-insecure-secret-key-for-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS should be set to the domain names your site will be served from
# For local development, you can use localhost and


ALLOWED_HOSTS = ['www.santenumeriquetchad.td','localhost', '127.0.0.1']
if DEBUG:
    ALLOWED_HOSTS += ['0.0.0.0'] #Pour la production


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
    'events',
    'candidature',
    'elearning',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Pour le support des langues
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'santenumerique.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'santenumerique.wsgi.application'
ASGI_APPLICATION = 'santenumerique.asgi.application'

AUTH_USER_MODEL = 'elearning.Utilisateur'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # Changer de mysql.backends en postgresql
        'NAME': os.environ.get('DJANGO_DB_NAME'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'HOST': os.environ.get('DJANGO_DB_HOST'),
        'PORT': os.environ.get('DJANGO_DB_PORT'),
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    # S'assurer que le moteur est PostgreSQL
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'



LANGUAGE_CODE = 'fr'  # Langue par défaut de votre projet

LANGUAGES = [ # Langues supportées par votre site
    ('fr', _('French')),
    ('en', _('English')),
    ('ar', _('Arabic')),
]

TIME_ZONE = 'Africa/Ndjamena'
USE_I18N = True
USE_TZ = True

# Configuration upload fichiers
MEDIA_URL = '/media/'
MEDIA_ROOT = '/vol/media/'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "webapp/static",]  # Si tu veux utiliser des fichiers statiques

STATIC_ROOT = '/vol/static/'


# Ensure this is included for static file discovery
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('ar', 'العربية'),
]
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'fr'  # Langue par défaut


if 'test' in sys.argv:
    # Configuration pour les tests
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    MEDIA_ROOT = '/tmp/test_media/'





LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/elearning/profile/'


if 'test' in sys.argv:
    # Configuration pour les tests (à conserver si vous avez des tests)
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    MEDIA_ROOT = '/tmp/test_media/'  # Répertoire temporaire pour les médias lors des tests
