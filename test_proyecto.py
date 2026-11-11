"""Script de prueba rápida del sistema de biblioteca"""
import sys
sys.path.insert(0, '.')

from modelo.modelos import Libro, Socio
from errores.errores import ErrorBiblioteca, LibroNoDisponibleError, SocioConLibroError

# --- Cargar datos ---
libros = {}
with open('datos/libros.txt', encoding='utf-8') as f:
    for linea in f:
        linea = linea.strip()
        if linea:
            l = Libro.desde_linea_txt(linea)
            libros[l.codigo] = l

socios = {}
with open('datos/socios.txt', encoding='utf-8') as f:
    for linea in f:
        linea = linea.strip()
        if linea:
            s = Socio.desde_linea_txt(linea)
            socios[s.codigo] = s

print(f"[OK] Libros cargados : {len(libros)}")
print(f"[OK] Socios cargados : {len(socios)}")

# --- Metodos personalizados ---
libro_prueba = libros['L010']
socio_prueba = socios['S001']
assert libro_prueba.esta_disponible(), "ERROR: deberia estar disponible"
assert not socio_prueba.tiene_libro_prestado(), "ERROR: socio no deberia tener libro"
print(f"[OK] Libro  : {libro_prueba.resumen_corto()}")
print(f"[OK] Socio  : {socio_prueba.nombre} | Tiene libro: {socio_prueba.tiene_libro_prestado()}")

# --- Prestamo simulado ---
libro_prueba.codigo_socio = socio_prueba.codigo
socio_prueba.codigo_libro = libro_prueba.codigo
assert not libro_prueba.esta_disponible()
assert socio_prueba.tiene_libro_prestado()
print(f"[OK] Prestamo: '{libro_prueba.titulo}' -> {socio_prueba.nombre}")

# --- Excepcion personalizada ---
try:
    raise LibroNoDisponibleError(libro_prueba.codigo, socio_prueba.codigo)
except ErrorBiblioteca as e:
    print(f"[OK] Excepcion personalizada -> codigo='{e.codigo}' | detalle='{e.detalle}'")

# --- Busqueda case-insensitive ---
termino = "quijote"
resultados = [l for l in libros.values() if termino.lower() in l.titulo.lower()]
print(f"[OK] Busqueda '{termino}': {[l.titulo for l in resultados]}")

# --- Serializacion ---
linea = libro_prueba.a_linea_txt()
libro_copia = Libro.desde_linea_txt(linea)
assert libro_copia.codigo == libro_prueba.codigo
print(f"[OK] Serializacion Libro OK: {linea}")

print()
print("=" * 45)
print("  TODOS LOS TESTS PASARON CORRECTAMENTE")
print("=" * 45)
