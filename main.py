# -*- coding: utf-8 -*-
"""
main.py - Sistema de Gestión de Biblioteca
==========================================
Módulo principal que gestiona el menú y la lógica de la aplicación.

Arquitectura:
    proyecto/
    ├── datos/
    │   ├── libros.txt
    │   └── socios.txt
    ├── errores/
    │   └── errores.py
    ├── modelo/
    │   └── modelos.py
    ├── log.txt
    └── main.py

Autor: Sistema generado para el Proyecto Final de Biblioteca
"""

import os
import sys
from datetime import datetime

# Forzar UTF-8 en la salida estándar (necesario en terminales Windows)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modelo.modelos import Libro, Socio
from errores.errores import (
    ErrorBiblioteca,
    LibroNoDisponibleError,
    SocioConLibroError,
    LibroNoEncontradoError,
    SocioNoEncontradoError,
    SocioSinLibroError,
    CodigoDuplicadoError,
)

# ---------------------------------------------------------------------------
# Rutas de ficheros
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_LIBROS = os.path.join(BASE_DIR, "datos", "libros.txt")
RUTA_SOCIOS = os.path.join(BASE_DIR, "datos", "socios.txt")
RUTA_LOG    = os.path.join(BASE_DIR, "log.txt")

# ---------------------------------------------------------------------------
# Colecciones en memoria
# ---------------------------------------------------------------------------
libros: dict[str, Libro] = {}
socios: dict[str, Socio] = {}


# ===========================================================================
# FUNCIONES DE LOG
# ===========================================================================

def registrar_log(evento: str, detalle: str) -> None:
    """
    Registra un evento en el fichero log.txt.

    Formato: [FECHA][EVENTO][DETALLE]

    Args:
        evento  (str): Nombre corto del evento (ej. 'PRÉSTAMO').
        detalle (str): Descripción detallada del evento.
    """
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha}][{evento}][{detalle}]\n"
    with open(RUTA_LOG, "a", encoding="utf-8") as f:
        f.write(linea)


# ===========================================================================
# FUNCIONES DE CARGA / GUARDADO
# ===========================================================================

def cargar_libros() -> None:
    """
    Carga los libros desde el fichero libros.txt en el diccionario global.
    Muestra un mensaje al usuario tras la carga.
    """
    global libros
    libros = {}
    try:
        with open(RUTA_LIBROS, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:  # ignorar líneas vacías
                    libro = Libro.desde_linea_txt(linea)
                    libros[libro.codigo] = libro
        print(f"  ✔ Se ha cargado la información de {len(libros)} libros correctamente.")
    except FileNotFoundError:
        print(f"  ⚠ No se encontró el fichero '{RUTA_LIBROS}'. Se iniciará sin libros.")


def cargar_socios() -> None:
    """
    Carga los socios desde el fichero socios.txt en el diccionario global.
    """
    global socios
    socios = {}
    try:
        with open(RUTA_SOCIOS, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    socio = Socio.desde_linea_txt(linea)
                    socios[socio.codigo] = socio
        print(f"  ✔ Se ha cargado la información de {len(socios)} socios correctamente.")
    except FileNotFoundError:
        print(f"  ⚠ No se encontró el fichero '{RUTA_SOCIOS}'. Se iniciará sin socios.")


def guardar_libros() -> None:
    """Vuelca el estado actual de los libros al fichero libros.txt."""
    with open(RUTA_LIBROS, "w", encoding="utf-8") as f:
        for libro in libros.values():
            f.write(libro.a_linea_txt() + "\n")


def guardar_socios() -> None:
    """Vuelca el estado actual de los socios al fichero socios.txt."""
    with open(RUTA_SOCIOS, "w", encoding="utf-8") as f:
        for socio in socios.values():
            f.write(socio.a_linea_txt() + "\n")


def guardar_todo() -> None:
    """Guarda libros y socios en sus ficheros correspondientes."""
    guardar_libros()
    guardar_socios()
    print("\n  ✔ Datos guardados correctamente en los ficheros.")
    registrar_log("CIERRE", "El sistema se cerró correctamente y los datos fueron guardados.")


# ===========================================================================
# HELPERS DE PRESENTACIÓN
# ===========================================================================

SEPARADOR = "=" * 70
SEP_FINO  = "-" * 70

def cabecera_tabla_libros() -> None:
    """Imprime la cabecera de la tabla de libros."""
    print(SEPARADOR)
    print(f"{'CÓD.':<6} {'TÍTULO':<36} {'AUTOR':<22} {'AÑO':>4}  {'ESTADO'}")
    print(SEP_FINO)

def fila_libro(libro: Libro) -> None:
    """Imprime una fila de la tabla con los datos de un libro."""
    titulo = (libro.titulo[:33] + "...") if len(libro.titulo) > 36 else libro.titulo
    autor  = (libro.autor[:19] + "...")  if len(libro.autor)  > 22 else libro.autor
    estado = "Disponible" if libro.esta_disponible() else f"→ {libro.codigo_socio}"
    print(f"{libro.codigo:<6} {titulo:<36} {autor:<22} {libro.anio:>4}  {estado}")


# ===========================================================================
# OPCIONES DEL MENÚ
# ===========================================================================

# ── Opción 1: Listar todos los libros ──────────────────────────────────────

def listar_todos_los_libros() -> None:
    """Muestra todos los libros con un formato de tabla."""
    print("\n  📚 TODOS LOS LIBROS DE LA BIBLIOTECA\n")
    cabecera_tabla_libros()
    for libro in libros.values():
        fila_libro(libro)
    print(SEPARADOR)
    print(f"  Total: {len(libros)} libros\n")


# ── Opción 2: Listar libros disponibles ───────────────────────────────────

def listar_libros_disponibles() -> None:
    """Muestra únicamente los libros no prestados."""
    disponibles = [l for l in libros.values() if l.esta_disponible()]
    print("\n  ✅ LIBROS DISPONIBLES\n")
    cabecera_tabla_libros()
    for libro in disponibles:
        fila_libro(libro)
    print(SEPARADOR)
    print(f"  Disponibles: {len(disponibles)} / {len(libros)}\n")


# ── Opción 3: Buscar libro por término ────────────────────────────────────

def buscar_libro_por_titulo() -> None:
    """
    Busca libros cuyo título contenga el término indicado (sin importar mayúsculas).
    """
    termino = input("\n  Introduce el término de búsqueda: ").strip()
    if not termino:
        print("  ⚠ No has introducido ningún término.")
        return

    resultados = [
        l for l in libros.values()
        if termino.lower() in l.titulo.lower()
    ]

    if not resultados:
        print(f"  ✖ No se encontró ningún libro con el término '{termino}'.\n")
        return

    print(f"\n  🔍 Resultados para '{termino}':\n")
    cabecera_tabla_libros()
    for libro in resultados:
        fila_libro(libro)
    print(SEPARADOR)
    print(f"  {len(resultados)} resultado(s) encontrado(s)\n")


# ── Opción 4: Prestar un libro ────────────────────────────────────────────

def prestar_libro() -> None:
    """
    Presta un libro a un socio.
    Gestiona los errores: libro ya prestado, socio ya tiene un libro.
    """
    print("\n  📖 PRÉSTAMO DE LIBRO\n")
    codigo_libro = input("  Código del libro  : ").strip().upper()
    codigo_socio = input("  Código del socio  : ").strip().upper()

    try:
        # Validar existencia del libro
        if codigo_libro not in libros:
            raise LibroNoEncontradoError(codigo_libro)

        # Validar existencia del socio
        if codigo_socio not in socios:
            raise SocioNoEncontradoError(codigo_socio)

        libro = libros[codigo_libro]
        socio = socios[codigo_socio]

        # Validar que el libro esté disponible
        if not libro.esta_disponible():
            raise LibroNoDisponibleError(codigo_libro, libro.codigo_socio)

        # Validar que el socio no tenga ya un libro
        if socio.tiene_libro_prestado():
            raise SocioConLibroError(codigo_socio, socio.codigo_libro)

        # Realizar el préstamo
        libro.codigo_socio = codigo_socio
        socio.codigo_libro = codigo_libro

        print(f"\n  ✔ Préstamo realizado: '{libro.titulo}' → {socio.nombre}\n")
        registrar_log(
            "PRÉSTAMO",
            f"Libro '{codigo_libro}' ({libro.titulo}) prestado al socio '{codigo_socio}' ({socio.nombre})"
        )

    except ErrorBiblioteca as e:
        # Usamos el atributo personalizado 'codigo' para identificar el tipo de error
        print(f"\n  ✖ Error [{e.codigo}]: {e.mensaje}")
        if e.detalle:
            print(f"     {e.detalle}")
        print()
        registrar_log("ERROR_PRÉSTAMO", str(e))


# ── Opción 5: Devolver un libro ───────────────────────────────────────────

def devolver_libro() -> None:
    """
    Devuelve el libro que tiene prestado un socio.
    Pide el código de socio y gestiona posibles errores.
    """
    print("\n  🔄 DEVOLUCIÓN DE LIBRO\n")
    codigo_socio = input("  Código del socio: ").strip().upper()

    try:
        if codigo_socio not in socios:
            raise SocioNoEncontradoError(codigo_socio)

        socio = socios[codigo_socio]

        if not socio.tiene_libro_prestado():
            raise SocioSinLibroError(codigo_socio)

        codigo_libro = socio.codigo_libro
        libro = libros.get(codigo_libro)

        # Limpiar el préstamo en socio
        socio.codigo_libro = None

        # Limpiar el préstamo en libro (si existe)
        if libro:
            libro.codigo_socio = None
            nombre_libro = libro.titulo
        else:
            nombre_libro = codigo_libro  # fallback si el libro fue eliminado

        print(f"\n  ✔ Devolución realizada: '{nombre_libro}' devuelto por {socio.nombre}\n")
        registrar_log(
            "DEVOLUCIÓN",
            f"Socio '{codigo_socio}' ({socio.nombre}) devolvió el libro '{codigo_libro}' ({nombre_libro})"
        )

    except ErrorBiblioteca as e:
        print(f"\n  ✖ Error [{e.codigo}]: {e.mensaje}")
        if e.detalle:
            print(f"     {e.detalle}")
        print()
        registrar_log("ERROR_DEVOLUCIÓN", str(e))


# ── Opción 6: Socios con libros prestados ─────────────────────────────────

def mostrar_socios_con_libros() -> None:
    """Muestra los socios que tienen algún libro en préstamo."""
    con_libro = [s for s in socios.values() if s.tiene_libro_prestado()]

    print("\n  👥 SOCIOS CON LIBRO EN PRÉSTAMO\n")
    if not con_libro:
        print("  (Ningún socio tiene libro prestado actualmente)\n")
        return

    print(f"  {'CÓD.':<6} {'NOMBRE':<30} {'LIBRO':>6}  {'TÍTULO'}")
    print(SEP_FINO)
    for socio in con_libro:
        libro = libros.get(socio.codigo_libro)
        titulo = libro.titulo if libro else "(no encontrado)"
        titulo_corto = (titulo[:30] + "...") if len(titulo) > 33 else titulo
        print(f"  {socio.codigo:<6} {socio.nombre:<30} {socio.codigo_libro:>6}  {titulo_corto}")
    print(SEP_FINO)
    print(f"  Total con préstamo: {len(con_libro)} socio(s)\n")


# ── Opción 7: Añadir socio o libro ────────────────────────────────────────

def aniadir_socio() -> None:
    """Permite añadir un nuevo socio al sistema."""
    print("\n  ➕ AÑADIR NUEVO SOCIO\n")
    codigo = input("  Código del socio (ej. S016): ").strip().upper()
    nombre = input("  Nombre completo            : ").strip()
    email  = input("  Email                      : ").strip()

    try:
        if codigo in socios:
            raise CodigoDuplicadoError("socio", codigo)

        nuevo_socio = Socio(codigo=codigo, nombre=nombre, email=email)
        socios[codigo] = nuevo_socio
        print(f"\n  ✔ Socio '{nombre}' añadido con código '{codigo}'.\n")
        registrar_log("NUEVO_SOCIO", f"Socio '{codigo}' ({nombre}, {email}) añadido al sistema.")

    except CodigoDuplicadoError as e:
        print(f"\n  ✖ Error [{e.codigo}]: {e.mensaje}")
        print(f"     {e.detalle}\n")


def aniadir_libro() -> None:
    """Permite añadir un nuevo libro al sistema."""
    print("\n  ➕ AÑADIR NUEVO LIBRO\n")
    codigo    = input("  Código del libro (ej. L101): ").strip().upper()
    titulo    = input("  Título                     : ").strip()
    autor     = input("  Autor                      : ").strip()
    anio_str  = input("  Año de publicación         : ").strip()
    categoria = input("  Categoría                  : ").strip()

    try:
        if codigo in libros:
            raise CodigoDuplicadoError("libro", codigo)

        # Validar año
        try:
            anio = int(anio_str)
        except ValueError:
            print(f"\n  ✖ El año '{anio_str}' no es un número válido.\n")
            return

        nuevo_libro = Libro(codigo=codigo, titulo=titulo, autor=autor,
                            anio=anio, categoria=categoria)
        libros[codigo] = nuevo_libro
        print(f"\n  ✔ Libro '{titulo}' añadido con código '{codigo}'.\n")
        registrar_log("NUEVO_LIBRO", f"Libro '{codigo}' ({titulo}, {autor}, {anio}) añadido al sistema.")

    except CodigoDuplicadoError as e:
        print(f"\n  ✖ Error [{e.codigo}]: {e.mensaje}")
        print(f"     {e.detalle}\n")


def menu_aniadir() -> None:
    """Submenú para añadir socios o libros."""
    print("\n  ¿Qué deseas añadir?")
    print("  [1] Socio")
    print("  [2] Libro")
    opcion = input("  Opción: ").strip()
    if opcion == "1":
        aniadir_socio()
    elif opcion == "2":
        aniadir_libro()
    else:
        print("  ⚠ Opción no válida.\n")


# ===========================================================================
# MENÚ PRINCIPAL
# ===========================================================================

MENU_TEXTO = """
╔══════════════════════════════════════════╗
║      SISTEMA DE GESTIÓN DE BIBLIOTECA    ║
╠══════════════════════════════════════════╣
║  1. Ver todos los libros                 ║
║  2. Ver libros disponibles               ║
║  3. Buscar libro por título              ║
║  4. Prestar un libro                     ║
║  5. Devolver un libro                    ║
║  6. Socios con libros prestados          ║
║  7. Añadir socio / libro                 ║
║  8. Salir y guardar                      ║
╚══════════════════════════════════════════╝
"""

OPCIONES = {
    "1": listar_todos_los_libros,
    "2": listar_libros_disponibles,
    "3": buscar_libro_por_titulo,
    "4": prestar_libro,
    "5": devolver_libro,
    "6": mostrar_socios_con_libros,
    "7": menu_aniadir,
}


def ejecutar_menu() -> None:
    """
    Bucle principal del menú. Se repite hasta que el usuario elige la opción 8.
    """
    while True:
        print(MENU_TEXTO)
        opcion = input("  Selecciona una opción (1-8): ").strip()

        if opcion == "8":
            guardar_todo()
            print("\n  👋 ¡Hasta pronto!\n")
            break
        elif opcion in OPCIONES:
            OPCIONES[opcion]()
        else:
            print("\n  ⚠ Opción no válida. Por favor elige entre 1 y 8.\n")


# ===========================================================================
# PUNTO DE ENTRADA
# ===========================================================================

def main() -> None:
    """Función principal: carga datos y arranca el menú."""
    print("\n" + "=" * 50)
    print("   📚 BIBLIOTECA - Iniciando el sistema...")
    print("=" * 50)
    cargar_libros()
    cargar_socios()
    print("=" * 50 + "\n")
    registrar_log("INICIO", "El sistema de biblioteca se ha iniciado.")
    ejecutar_menu()


if __name__ == "__main__":
    main()
