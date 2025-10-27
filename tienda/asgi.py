"""
Archivo ASGI del proyecto.

ASGI = Asynchronous Server Gateway Interface.
Permite que Django trabaje con conexiones asíncronas
(WebSockets, HTTP/2, chat en tiempo real, etc.)
"""

import os
from django.core.asgi import get_asgi_application

# Define qué archivo de configuración (settings.py) se usará
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')

# Crea la aplicación ASGI para que el servidor web se comunique con Django
application = get_asgi_application()