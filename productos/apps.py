# ======================================================
# Configuración de la aplicación 'productos' para Django
# ======================================================
from django.apps import AppConfig


class ProductosConfig(AppConfig):
    # Tipo de campo por defecto para las claves primarias de los modelos
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la aplicación dentro del proyecto Django
    name = 'productos'
