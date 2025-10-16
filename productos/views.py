# ======================================================
# Imports necesarios para vistas y utilidades de Django
# ======================================================
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from .models import Producto, Carrito, CarritoProducto, Categoria, Pedido, PedidoProducto
from .forms import RegistroForm
import mercadopago
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# ======================================================
# Vistas de productos
# - Detalle de producto, lista de productos
# ======================================================
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    productos_similares = Producto.objects.filter(categoria=producto.categoria).exclude(id=producto.id)[:8]
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'productos_similares': productos_similares,
    })


def lista_productos(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'productos/lista.html', {'productos': productos, 'categorias': categorias})