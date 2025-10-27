"""
Archivo WSGI para el proyecto.

WSGI = Web Server Gateway Interface.
Sirve para que servidores web (ej: Gunicorn, uWSGI) 
puedan comunicarse con la app Django.
"""

import os
from django.core.wsgi import get_wsgi_application

# Indica qué archivo de configuración (settings.py) se usará
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')

# Crea la aplicación WSGI que el servidor usará para ejecutar Django
application = get_wsgi_application()