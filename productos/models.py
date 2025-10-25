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



# ======================================================
# Modelo Carrito
# - Representa el carrito de un usuario
# - Relación ManyToMany con productos a través de CarritoProducto
# - Permite calcular total
# ======================================================
class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto', blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.carritoproducto_set.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username} ({self.carritoproducto_set.count()} productos)"

    class Meta:
        db_table = 'carritos_usuarios'
        verbose_name = "Carrito (de cada usuario)"
        verbose_name_plural = "Carritos (de cada usuario)"


# ======================================================
# Modelo CarritoProducto
# - Intermedia entre Carrito y Producto
# - Almacena cantidad y calcula subtotal
# ======================================================
class CarritoProducto(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio_con_descuento * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Carrito de {self.carrito.usuario.username})"

    class Meta:
        db_table = 'carritos_productos'
        verbose_name = "Producto en Carrito (contenido del carrito)"
        verbose_name_plural = "Productos en Carrito (contenido del carrito)"


# ======================================================
# Modelo Pedido
# - Representa un pedido realizado por un usuario
# - Relación ManyToMany con Producto a través de PedidoProducto
# - Calcula número de pedido secuencial
# ======================================================
class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField('Producto', through='PedidoProducto')
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    pagado = models.BooleanField(default=False)
    numero_pedido = models.PositiveIntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            ultimo = Pedido.objects.order_by('-numero_pedido').first()
            self.numero_pedido = (ultimo.numero_pedido + 1) if ultimo and ultimo.numero_pedido else 1
        super().save(*args, **kwargs)

    def numero_pedido_formateado(self):
        return str(self.numero_pedido).zfill(5)

    def __str__(self):
        return f"Pedido #{self.numero_pedido_formateado()} - {self.usuario.username}"

    class Meta:
        db_table = 'pedidos_usuarios'
        verbose_name = "Pedido (compra confirmada)"
        verbose_name_plural = "Pedidos (compras confirmadas)"


# ======================================================
# Modelo PedidoProducto
# - Intermedia entre Pedido y Producto
# - Almacena cantidad y precio unitario
# ======================================================
class PedidoProducto(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def subtotal(self):
        return (self.precio_unitario or 0) * (self.cantidad or 0)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.numero_pedido_formateado()})"

    class Meta:
        db_table = 'pedidos_productos'
        verbose_name = "Producto en Pedido (contenido del pedido)"
        verbose_name_plural = "Productos en Pedido (contenido del pedido)"


# ======================================================
# Modelo Perfil
# - Información adicional del usuario
# - Teléfono desglosado en código y número
# ======================================================
class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telefono_codigo = models.CharField(max_length=5, blank=True, null=True, help_text="Ej: +54")
    telefono_numero = models.CharField(max_length=15, blank=True, null=True, help_text="Ej: 113456789")

    def __str__(self):
        return f"Perfil de {self.user.username}"

    class Meta:
        db_table = 'perfiles_usuarios'
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"


# ======================================================
# Modelo Usuario
# - Extiende AbstractUser agregando teléfono
# - Configura related_name para permisos y grupos
# ======================================================
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='productos_usuario_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='productos_usuario_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'datos_usuarios'
        verbose_name = "Usuario (persona que usa el sistema)"
        verbose_name_plural = "Usuarios (personas que usan el sistema)"
