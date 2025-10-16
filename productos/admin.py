# ======================================================
# Imports necesarios para el admin de Django
# ======================================================
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Importación de modelos y formularios personalizados
from .models import (
    Producto, Categoria, Carrito, CarritoProducto, 
    ProductoImagen, Usuario, Pedido, PedidoProducto
)
from .forms import UsuarioCreationForm

# ======================================================
# Admin de Categorías
# - Muestra nombre y cantidad de productos asociados
# - Permite búsqueda por nombre
# ======================================================
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cantidad_productos")
    search_fields = ("nombre",)

    def cantidad_productos(self, obj):
        return obj.productos.count()
    cantidad_productos.short_description = "Cantidad de productos"

admin.site.register(Categoria, CategoriaAdmin)

# ======================================================
# Inline de imágenes adicionales de Productos
# - Permite subir varias imágenes extra para un producto
# ======================================================
class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ["imagen"]

# ======================================================
# Admin de Productos
# - Muestra información clave: nombre, precio, stock, categoría
# - Permite búsqueda, filtros y carga de imágenes adicionales
# ======================================================
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock", "categoria")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria", "stock")
    inlines = [ProductoImagenInline]

    fieldsets = (
        ("Información básica", {
            "fields": ("nombre", "descripcion", "categoria")
        }),
        ("Precio y stock", {
            "fields": ("precio", "descuento", "stock")
        }),
        ("Imagen principal", {
            "fields": ("imagen",)
        }),
        ("Imágenes adicionales", {
            "fields": (),
            "description": "Agregar imágenes adicionales en la sección de abajo"
        }),
    )

admin.site.register(Producto, ProductoAdmin)