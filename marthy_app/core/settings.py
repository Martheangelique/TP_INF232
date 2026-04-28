import os
from pathlib import Path

# 1. Chemins de base (Base Directory)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Sécurité
# En production, gardez cette clé secrète !
SECRET_KEY = 'django-insecure-votre-cle-secrete-specifique-au-projet'

# DEBUG = True pour le développement dans VS Code
DEBUG = True

# Autorise l'adresse spécifique de ngrok ou toutes les adresses (*)
ALLOWED_HOSTS = ['cryptic-pacifier-gradation.ngrok-free.dev', '127.0.0.1', 'localhost']

# 3. Définition des applications (Inclusion de 'surveillance')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Votre application métier pour la collecte de données
    'surveillance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# 4. Configuration des Templates (HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # On définit le dossier global des templates
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
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

WSGI_APPLICATION = 'core.wsgi.application'

# 5. Base de données
# Utilisation de SQLite par défaut (parfait pour le développement local)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 6. Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 7. Localisation (Configuration pour le contexte camerounais)
LANGUAGE_CODE = 'fr-fr' # Langue française

TIME_ZONE = 'Africa/Douala' # Fuseau horaire du Cameroun

USE_I18N = True

USE_TZ = True

# 8. Fichiers Statiques (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Dossier où les fichiers seront rassemblés pour la production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 9. Type de champ d'ID par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'