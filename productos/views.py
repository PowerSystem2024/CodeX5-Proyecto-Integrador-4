# ======================================================
# Imports necesarios para vistas y utilidades de Django
# ======================================================
import io
import random
import time

import mercadopago
from django.conf import settings
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .forms import RegistroForm
from .models import Producto, Carrito, CarritoProducto, Categoria, Pedido, PedidoProducto


# ======================================================
# Función auxiliar para registrar cambios en el admin
# ======================================================
def registrar_cambio_admin(user, objeto, descripcion="Cambio realizado desde la vista"):
    """
    Permite crear un registro de cambio en el admin de Django
    para cualquier objeto, útil para auditoría o seguimiento.
    """
    content_type = ContentType.objects.get_for_model(objeto)
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=content_type.id,
        object_id=objeto.id,
        object_repr=str(objeto),
        action_flag=CHANGE,
        change_message=descripcion
    )


# ======================================================
# Vistas de cuenta de usuario
# - Mi cuenta, ver datos, historial de compras
# ======================================================
@login_required
def mi_cuenta(request):
    return render(request, 'productos/mi_cuenta.html')


@login_required
def ver_datos_usuario(request):
    return render(request, 'productos/ver_datos_usuario.html', {'user': request.user})


@login_required
def historial_compras(request):
    pedidos = request.user.pedido_set.order_by('-fecha').all()
    return render(request, 'productos/historial_compras.html', {'pedidos': pedidos})


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


# ======================================================
# Vistas de carrito de compras
# - Agregar, ver, eliminar producto y vaciar carrito
# ======================================================
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock <= 0:
        return redirect('lista_productos')

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:
        if carrito_producto.cantidad < producto.stock:
            carrito_producto.cantidad += 1
            carrito_producto.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'lista_productos'))


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    total = carrito.total()
    return render(request, 'productos/carrito.html', {'carrito': carrito, 'total': total})


@login_required
def eliminar_del_carrito(request, producto_id):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    item = CarritoProducto.objects.filter(carrito=carrito, producto=producto).first()

    if item:
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
    
    return redirect('ver_carrito')


@login_required
def vaciar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.carritoproducto_set.all().delete()
    return redirect('ver_carrito')


# ======================================================
# Vistas de checkout con Mercado Pago
# - Crea preferencia de pago y devuelve URL
# ======================================================
@login_required
def checkout(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    total = carrito.total()

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        direccion = request.POST.get('direccion', '')
        request.session['direccion_envio'] = direccion

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        items = []
        for item in carrito.carritoproducto_set.all():
            items.append({
                "title": item.producto.nombre,
                "quantity": item.cantidad,
                "unit_price": float(item.producto.precio_con_descuento),
                "currency_id": "ARS",
            })

        external_reference = f"ORDER_{int(time.time())}_{random.randint(1000,9999)}"
        
        preference_data = {
            "items": items,
            "payer": {"email": request.user.email},
            "external_reference": external_reference,
            "back_urls": {
                "success": request.build_absolute_uri("/checkout/success/manual/"),
                "failure": request.build_absolute_uri("/checkout/failure/"),
                "pending": request.build_absolute_uri("/checkout/pending/"),
            },
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response.get("response", {})
            url = preference.get("sandbox_init_point")
            if not url:
                error_info = preference_response.get("cause", [])
                return JsonResponse({'error': True, 'message': f'Error de MercadoPago: {error_info}'})
            
            return HttpResponse(url)
            
        except Exception as e:
            return JsonResponse({'error': True, 'message': f'Error interno: {str(e)}'})

    return render(request, 'productos/checkout.html', {'carrito': carrito, 'total': total})


# ======================================================
# Vista de pago aprobado / checkout exitoso
# - Crea Pedido y PedidoProducto
# - Reduce stock de productos
# - Genera PDF de factura
# - Muestra la página de pago aprobado
# ======================================================
@login_required
@login_required
def pago_aprobado(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    direccion = request.session.get('direccion_envio', '')

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not carrito.carritoproducto_set.exists():
            return JsonResponse({'status': 'error', 'message': 'No hay productos en el carrito.'})

        try:
            # Crear el pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                total=carrito.total(),
                pagado=True,
                direccion_envio=direccion
            )

            # Crear los items del pedido y actualizar stock
            for item in carrito.carritoproducto_set.all():
                PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio_con_descuento
                )
                item.producto.stock = max(item.producto.stock - item.cantidad, 0)
                item.producto.save()

            # Vaciar carrito y limpiar sesión
            carrito.carritoproducto_set.all().delete()
            request.session.pop('direccion_envio', None)

            # Generar PDF de factura
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            fecha_str = timezone.localtime(pedido.fecha).strftime("%d/%m/%Y %H:%M")

            elements.append(Paragraph(f"Factura - Pedido #{pedido.numero_pedido_formateado()}", styles['Title']))
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"<b>Cliente:</b> {pedido.usuario.first_name} {pedido.usuario.last_name}", styles['Normal']))
            elements.append(Paragraph(f"<b>Email:</b> {pedido.usuario.email}", styles['Normal']))
            elements.append(Paragraph(f"<b>Dirección:</b> {pedido.direccion_envio}", styles['Normal']))
            elements.append(Paragraph(f"<b>Fecha:</b> {fecha_str}", styles['Normal']))
            elements.append(Spacer(1, 12))

            cell_style = ParagraphStyle(name='cell_style', fontName='Helvetica', fontSize=10, leading=12, alignment=TA_LEFT)

            data = [['Producto', 'Cantidad', 'Precio Unitario', 'Subtotal']]
            for item in pedido.pedidoproducto_set.all():
                subtotal = item.cantidad * item.precio_unitario
                producto_parrafo = Paragraph(item.producto.nombre, cell_style)
                data.append([producto_parrafo, str(item.cantidad), f"${item.precio_unitario:.2f}", f"${subtotal:.2f}"])
            data.append(['', '', 'Total:', f"${pedido.total:.2f}"])

            table = Table(data, colWidths=[200, 60, 100, 100], repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('ALIGN',(1,1),(-1,-1),'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ]))
            elements.append(table)

            doc.build(elements)
            buffer.seek(0)

            pdf_filename = f"pedido_{pedido.numero_pedido_formateado()}.pdf"
            pdf_path = f"static/media/pedidos/{pdf_filename}"
            with open(pdf_path, "wb") as f:
                f.write(buffer.getbuffer())

            # Devolver JSON con la URL del PDF
            return JsonResponse({
                'status': 'ok',
                'message': 'Pedido generado correctamente.',
                'pdf_url': f"/{pdf_path}"
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error al generar el pedido: {str(e)}'})

    return render(request, "productos/pago_aprobado.html", {'carrito': carrito})


# ======================================================
# Vistas de autenticación
# - Registro, login y logout
# ======================================================
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista_productos')
    else:
        form = RegistroForm()
    
    return render(request, 'productos/registro.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('lista_productos')
    else:
        form = AuthenticationForm()
    return render(request, 'productos/login.html', {'form': form})


@login_required
def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')


# ======================================================
# Vista de historial de pedidos del usuario
# ======================================================
@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'productos/historial.html', {'pedidos': pedidos})
