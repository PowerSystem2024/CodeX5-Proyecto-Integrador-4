"""
Script para cargar automáticamente las imágenes adicionales de productos.
Este script busca imágenes con patrones .2.jpg y .3.jpg y las asocia
al producto correspondiente en la tabla ProductoImagen.
"""

import os
import sys
import django

# Configurar Django para poder usar los modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
django.setup()

from productos.models import Producto, ProductoImagen

def cargar_imagenes_adicionales():
    """
    Recorre todos los productos y busca imágenes adicionales en media/img_productos/
    con los patrones: {id}.2.jpg, {id}.3.jpg
    """
    # Limpiar imágenes adicionales existentes
    ProductoImagen.objects.all().delete()
    print("✓ Imágenes adicionales previas eliminadas")
    
    productos = Producto.objects.all()
    total_cargadas = 0
    
    for producto in productos:
        # Buscar imágenes adicionales para este producto
        # Patrones: 1.2.jpg, 1.3.jpg, 2.2.jpg, etc.
        for sufijo in ['.2.jpg', '.3.jpg']:
            nombre_archivo = f"{producto.id}{sufijo}"
            ruta_imagen = f"img_productos/{nombre_archivo}"
            
            # Verificar si el archivo existe
            ruta_completa = os.path.join('media', ruta_imagen)
            if os.path.exists(ruta_completa):
                # Crear la entrada en ProductoImagen
                ProductoImagen.objects.create(
                    producto=producto,
                    imagen=ruta_imagen
                )
                total_cargadas += 1
                print(f"  ✓ Agregada imagen {ruta_imagen} al producto: {producto.nombre}")
    
    print(f"\n{'='*60}")
    print(f"Total de imágenes adicionales cargadas: {total_cargadas}")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("Iniciando carga de imágenes adicionales...")
    print(f"{'='*60}")
    cargar_imagenes_adicionales()
    print("\n✓ Proceso completado exitosamente")
