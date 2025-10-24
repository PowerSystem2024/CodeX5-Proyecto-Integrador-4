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
    
    # Registro y autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),


      # Detalle de producto
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto')
    
        # Área de usuario
    path('mi_cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('mi_cuenta/datos/', views.ver_datos_usuario, name='ver_datos_usuario'),
    path('mi_cuenta/historial/', views.historial_compras, name='historial_compras'),
]