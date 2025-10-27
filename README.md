# 🛒 E-Commerce CodeX5 - Proyecto Final

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Deployed](https://img.shields.io/badge/Deployed-Render-success)

## 📋 Descripción

**E-Commerce CodeX5** es el Proyecto Final desarrollado por el grupo **CodeX5** para la **Tecnicatura Universitaria en Programación (TUP)** de la **Universidad UTN San Rafael**.

Es una tienda online completa especializada en productos de tecnología y gaming, desarrollada con Django y desplegada en producción.

🌐 **Visitar el sitio:** [https://codex5-proyecto-integrador-4.onrender.com/](https://codex5-proyecto-integrador-4.onrender.com/)

---

## ✨ Características Principales

### 🔐 Autenticación de Usuarios
- Registro e inicio de sesión seguro
- Gestión de sesiones persistentes
- Panel de cuenta personalizado

### 🛍️ Catálogo de Productos
- Sistema de categorías (Monitores, Sillas, Mouse, Teclados, Placas de Video)
- Buscador por nombre y descripción
- Galería de imágenes con miniaturas
- Sistema de descuentos
- Indicadores de stock en tiempo real
- Productos similares sugeridos

### 🛒 Carrito de Compras
- Agregar y modificar cantidades
- Validación automática de stock
- Cálculo de totales en tiempo real
- Persistencia del carrito por usuario

### 💳 Sistema de Pagos
- Integración con Mercado Pago
- Checkout seguro
- Confirmación automática de pagos vía webhook
- Actualización de stock al confirmar compra

### 📦 Gestión de Pedidos
- Historial completo de compras
- Generación de facturas en PDF
- Seguimiento de estados de pedido

### 🎨 Diseño
- Interfaz moderna y responsive
- Adaptable a móviles, tablets y escritorio
- Navegación intuitiva

### 🔧 Panel de Administración
- Gestión completa de productos y categorías
- Control de usuarios y permisos
- Visualización de carritos y pedidos
- Sistema de auditoría

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.11** + **Django 5.0**
- **PostgreSQL** (producción) / **SQLite** (desarrollo)
- **HTML5**, **CSS3**, **JavaScript**
- **Mercado Pago SDK** - Pasarela de pagos
- **ReportLab** - Generación de PDFs
- **Render** - Hosting
- **WhiteNoise** - Archivos estáticos
- **Gunicorn** - Servidor WSGI

---

## 📦 Estructura del Proyecto

```
CodeX5-Proyecto-Integrador-4/
│
├── productos/              # App principal del e-commerce
│   ├── models.py          # Modelos (Producto, Carrito, Pedido, etc.)
│   ├── views.py           # Vistas y lógica de negocio
│   ├── forms.py           # Formularios (Registro, Login)
│   ├── urls.py            # Rutas de la app
│   ├── admin.py           # Configuración del panel admin
│   ├── templates/         # Plantillas HTML
│   │   └── productos/
│   │       ├── base.html
│   │       ├── lista.html
│   │       ├── detalle_producto.html
│   │       ├── carrito.html
│   │       ├── checkout.html
│   │       ├── mi_cuenta.html
│   │       ├── historial_compras.html
│   │       ├── login.html
│   │       └── registro.html
│   └── migrations/        # Migraciones de BD
│
├── tienda/                # Configuración del proyecto
│   ├── settings.py        # Configuraciones principales
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Punto de entrada WSGI
│
├── static/                # Archivos estáticos
│   ├── css/               # Estilos CSS
│   └── img_productos/     # Imágenes de productos
│
├── media/                 # Archivos multimedia
│   └── img_productos/     # Imágenes subidas
│
├── fixtures/              # Datos iniciales
│   ├── categorias_fixture.json
│   └── productos_fixture.json
│
├── scripts/               # Scripts auxiliares
│   └── cargar_imagenes_extra.py
│
├── requirements.txt       # Dependencias Python
├── manage.py             # Comando de Django
└── db.sqlite3            # Base de datos local
```

---

## 🚀 Instalación y Configuración Local

### Prerrequisitos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/PowerSystem2024/CodeX5-Proyecto-Integrador-4.git
cd CodeX5-Proyecto-Integrador-4
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

En Windows:
```bash
venv\Scripts\activate
```

En Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**

Crear archivo `.env` con:
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
MP_ACCESS_TOKEN=tu-token-de-mercadopago
MP_PUBLIC_KEY=tu-clave-publica-de-mercadopago
```

6. **Aplicar migraciones**
```bash
python manage.py migrate
```

7. **Cargar datos iniciales**
```bash
python manage.py loaddata fixtures/categorias_fixture.json
python manage.py loaddata fixtures/productos_fixture.json
```

8. **Crear superusuario**
```bash
python manage.py createsuperuser
```

9. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

10. **Acceder a la aplicación**
- Sitio web: `http://localhost:8000`
- Panel admin: `http://localhost:8000/admin`

---

## 🎯 Funcionalidades Destacadas

### 💰 Sistema de Descuentos
- Cálculo automático de descuentos
- Visualización de ahorro total
- Badges con porcentaje de descuento

### 📊 Validación de Stock
- Verificación antes de agregar al carrito
- Actualización automática al confirmar compra
- Alertas visuales de disponibilidad

### 📄 Facturas en PDF
- Generación automática de comprobantes
- Descarga desde el historial de compras
- Información detallada de productos y totales


---

## 📊 Base de Datos

El proyecto utiliza los siguientes modelos principales:
- **Usuario** - Gestión de cuentas (extendido de AbstractUser)
- **Categoría** - Organización de productos
- **Producto** - Información de artículos (precio, stock, descuento, imágenes)
- **Carrito** - Productos seleccionados por usuario
- **Pedido** - Registro de compras realizadas

---

## 🤝 Equipo CodeX5

Proyecto desarrollado por el grupo **CodeX5** como Proyecto Final de la **Tecnicatura Universitaria en Programación (TUP)** - **Universidad UTN San Rafael**.

### 👥 Integrantes
- **Santiago Calzolari**
- **Ana Castro**
- **Leonel Palominos**
- **Santino Salatino**

---


## 🔗 Links Útiles

- 🌐 **Sitio en Producción:** [https://codex5-proyecto-integrador-4.onrender.com/](https://codex5-proyecto-integrador-4.onrender.com/)
- 📦 **Repositorio:** [GitHub - CodeX5-Proyecto-Integrador-4](https://github.com/PowerSystem2024/CodeX5-Proyecto-Integrador-4)
- 📚 **Django Documentation:** [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- 💳 **Mercado Pago Developers:** [https://www.mercadopago.com.ar/developers](https://www.mercadopago.com.ar/developers)

---



**¡Gracias por visitar nuestro proyecto! 🚀**

> *Desarrollado con ❤️ por CodeX5*
