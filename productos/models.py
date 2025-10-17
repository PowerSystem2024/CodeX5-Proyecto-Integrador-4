# ======================================================
# Imports necesarios para modelos de Django
# ======================================================
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# ======================================================
# Modelo Categoria
# - Representa categorías para organizar productos
# - Tiene nombre único
# ======================================================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categorias_productos'
        verbose_name = "Categoría (para organizar productos)"
        verbose_name_plural = "Categorías (para organizar productos)"


# ======================================================
# Modelo Producto
# - Representa un producto con precio, stock, descuento
# - Relación con Categoria
# - Permite calcular precio con descuento y ahorro
# ======================================================
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to="img_productos/", blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="productos",
        null=True,
        blank=True
    )

    @property
    def precio_con_descuento(self):
        return self.precio - (self.precio * self.descuento / 100) if self.descuento else self.precio

    @property
    def ahorro(self):
        return self.precio * self.descuento / 100 if self.descuento else 0

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

    class Meta:
        db_table = 'productos'
        verbose_name = "Producto (artículo a la venta)"
        verbose_name_plural = "Productos (artículos a la venta)"


# ======================================================
# Modelo ProductoImagen
# - Permite asociar múltiples imágenes a un producto
# ======================================================
class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='img_productos/', blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

    class Meta:
        db_table = 'imagenes_productos'
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"
