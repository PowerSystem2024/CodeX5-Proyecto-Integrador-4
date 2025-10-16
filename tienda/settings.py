"""
Archivo de configuración principal de Django (settings.py).
Define cómo funciona el proyecto: apps instaladas, base de datos, 
archivos estáticos, seguridad, etc.
"""

import os
from pathlib import Path
import dj_database_url  # Permite configurar la base de datos a partir de una URL (útil en Render/Heroku)

# === RUTAS DEL PROYECTO ===
# BASE_DIR representa la carpeta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


# === SEGURIDAD Y DEBUG ===
# Clave secreta usada para encriptar datos (no debe compartirse en producción)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-a*rrx*8n6q6l=v%y4ze45^w0=(dt7(efc9hpmzx@!lf1a+z$h1')

# Modo de depuración: True = muestra errores detallados (solo en desarrollo)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Lista de dominios permitidos para acceder al proyecto
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'proyectoecommerce.onrender.com']


# === APLICACIONES INSTALADAS ===
# Apps de Django que se usarán + la app personalizada "productos"
INSTALLED_APPS = [
    'django.contrib.admin',        # Panel de administración
    'django.contrib.auth',         # Sistema de autenticación
    'django.contrib.contenttypes', # Tipos de contenido
    'django.contrib.sessions',     # Manejo de sesiones
    'django.contrib.messages',     # Sistema de mensajes
    'django.contrib.staticfiles',  # Archivos estáticos (CSS, JS, imágenes)
    'productos',                   # App principal del e-commerce
]

# === MIDDLEWARE ===
# Capas que procesan cada petición/respuesta
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Permite servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # Protege contra ataques CSRF en formularios
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === CONFIGURACIÓN DE URLs Y WSGI ===
ROOT_URLCONF = 'tienda.urls'         # Archivo principal de rutas (urls.py)
WSGI_APPLICATION = 'tienda.wsgi.application'  # Servidor WSGI (para producción con Gunicorn, etc.)


# === TEMPLATES ===
# Define dónde están los archivos HTML y cómo se renderizan
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],      # Directorios extra de templates (aquí está vacío)
        'APP_DIRS': True, # Busca templates dentro de cada app
        'OPTIONS': {
            'context_processors': [  # Funciones que inyectan info global a los templates
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# === BASE DE DATOS ===
# Usa dj_database_url para conectarse a PostgreSQL (producción) o SQLite (desarrollo por defecto)
DATABASES = {
    'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}


# === VALIDACIÓN DE CONTRASEÑAS ===
# Reglas que se aplican al crear o cambiar contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',}, # Requiere longitud mínima
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',}, # Evita contraseñas comunes
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',}, # Evita que sea solo numérica
]


# === CONFIGURACIÓN REGIONAL ===
LANGUAGE_CODE = 'en-us'                           # Idioma por defecto
TIME_ZONE = 'America/Argentina/Buenos_Aires'      # Zona horaria
USE_I18N = True                                   # Traducción de textos
USE_TZ = True                                     # Manejo de zonas horarias


# === ARCHIVOS ESTÁTICOS (CSS, JS, Imágenes) ===
STATIC_URL = '/static/'                      # URL de acceso
STATICFILES_DIRS = [BASE_DIR / 'static']     # Carpeta donde están los archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'       # Carpeta donde se copian para producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Optimiza estáticos

# === ARCHIVOS MULTIMEDIA (subidos por usuarios, ej: imágenes de productos) ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Opciones extra de WhiteNoise para servir archivos en producción
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True


# === CONFIGURACIÓN DE LOGIN ===
LOGIN_URL = '/login/'          # Redirige aquí si no está logueado
LOGIN_REDIRECT_URL = '/'       # A dónde va después de iniciar sesión


# === CONFIGURACIÓN DE MODELOS ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'productos.Usuario'  # Usa un modelo de usuario personalizado definido en la app productos


# === CONFIGURACIÓN DE MERCADO PAGO ===
# Tokens de prueba (sandbox). En producción deben ir en variables de entorno.
MP_ACCESS_TOKEN = os.environ.get('MP_ACCESS_TOKEN', 'APP_USR-659340762835775-091415-d107d619602a205f2ceef439eb3bbfb4-2669198849')
MP_PUBLIC_KEY = os.environ.get('MP_PUBLIC_KEY', 'APP_USR-f00f52bd-6145-4161-8a5f-21feda075d81')