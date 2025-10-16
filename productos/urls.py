# ================================
# Importar Django y vistas locales
# ================================
from django.urls import path
from . import views

# ================================
# URLs de la app 'productos'
# ================================
urlpatterns = [
    # Página principal: lista de productos
    path('', views.lista_productos, name='lista_productos'),

      # Detalle de producto
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto')
]