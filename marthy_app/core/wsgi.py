import os
from django.core.wsgi import get_wsgi_application

# On indique à Django où se trouve le fichier settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()