# Importa las configuraciones definidas en settings.py
from django.conf import settings

# Importa una función que permite servir archivos estáticos (imágenes, PDFs, etc.)
from django.conf.urls.static import static

# Importa la interfaz de administración de Django
from django.contrib import admin

# Importa funciones para definir las rutas (URLs) del proyecto
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),           # Panel de administración
    path('', include('productos.urls')),       # Rutas principales de la app productos
]

# Permite mostrar archivos multimedia (imágenes, PDFs, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)