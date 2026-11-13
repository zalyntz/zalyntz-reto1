# -*- coding: utf-8 -*-
"""
main.py - Sistema de Gestion de Biblioteca
Punto de entrada de la aplicacion.
"""

import os
import sys

from datetime import datetime
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

# Rutas de los ficheros de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_LIBROS = os.path.join(BASE_DIR, "datos", "libros.txt")
RUTA_SOCIOS = os.path.join(BASE_DIR, "datos", "socios.txt")
RUTA_LOG    = os.path.join(BASE_DIR, "log.txt")

# Diccionarios para guardar los datos en memoria
libros = {}
socios = {}


# =====================================================================
# FUNCION PARA EL LOG DE ACTIVIDAD
# Guarda los eventos en log.txt con formato [Fecha][nombre del evento][detalles]
# =====================================================================

def registrar_log(evento, detalle):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha_actual}][{evento}][{detalle}]\n"
    with open(RUTA_LOG, "a", encoding="utf-8") as f:
        f.write(linea)


# =====================================================================
# FUNCIONES PARA CARGAR Y GUARDAR FICHEROS TXT
# =====================================================================

def cargar_libros():
    # Carga los libros desde libros.txt
    global libros
    libros = {}
    try:
        with open(RUTA_LIBROS, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    libro = Libro.desde_linea_txt(linea)
                    libros[libro.codigo] = libro
        print(f"Se ha cargado la informacion de {len(libros)} libros correctamente.")
    except FileNotFoundError:
        print(f"Aviso: No se ha encontrado el archivo {RUTA_LIBROS}.")


def cargar_socios():
    # Carga los socios desde socios.txt
    global socios
    socios = {}
    try:
        with open(RUTA_SOCIOS, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    socio = Socio.desde_linea_txt(linea)
                    socios[socio.codigo] = socio
        print(f"Se ha cargado la informacion de {len(socios)} socios correctamente.")
    except FileNotFoundError:
        print(f"Aviso: No se ha encontrado el archivo {RUTA_SOCIOS}.")


def guardar_libros():
    # Guarda los libros en libros.txt
    with open(RUTA_LIBROS, "w", encoding="utf-8") as f:
        for libro in libros.values():
            f.write(libro.a_linea_txt() + "\n")


def guardar_socios():
    # Guarda los socios en socios.txt
    with open(RUTA_SOCIOS, "w", encoding="utf-8") as f:
        for socio in socios.values():
            f.write(socio.a_linea_txt() + "\n")


def guardar_todo():
    # Guarda libros y socios en sus ficheros
    guardar_libros()
    guardar_socios()
    print("\nDatos guardados correctamente en los ficheros.")
    registrar_log("CIERRE", "El sistema se cerro correctamente y se guardaron los datos.")


# =====================================================================
# FUNCIONES DE FORMATO Y MOSTRAR DATOS
# =====================================================================

def imprimir_cabecera_libros():
    print("=" * 75)
    print(f"{'COD.':<6} {'TITULO':<35} {'AUTOR':<20} {'AÑO':>4}  {'ESTADO'}")
    print("-" * 75)

def imprimir_fila_libro(libro):
    titulo = (libro.titulo[:32] + "...") if len(libro.titulo) > 35 else libro.titulo
    autor  = (libro.autor[:17] + "...")  if len(libro.autor)  > 20 else libro.autor
    estado = "Disponible" if libro.esta_disponible() else f"Prestado -> {libro.codigo_socio}"
    print(f"{libro.codigo:<6} {titulo:<35} {autor:<20} {libro.anio:>4}  {estado}")


# Opcion 1: Listar todos los libros
def listar_todos_los_libros():
    print("\n--- LISTA DE TODOS LOS LIBROS ---")
    imprimir_cabecera_libros()
    for libro in libros.values():
        imprimir_fila_libro(libro)
    print("=" * 75)
    print(f"Total: {len(libros)} libros en la biblioteca\n")


# Opcion 2: Listar libros disponibles
def listar_libros_disponibles():
    disponibles = [l for l in libros.values() if l.esta_disponible()]
    print("\n--- LIBROS DISPONIBLES ---")
    imprimir_cabecera_libros()
    for libro in disponibles:
        imprimir_fila_libro(libro)
    print("=" * 75)
    print(f"Disponibles: {len(disponibles)} de {len(libros)}\n")


# Opcion 3: Buscar libro por titulo (sin distinguir mayusculas/minusculas)
def buscar_libro_por_titulo():
    termino = input("\nIntroduce el texto a buscar en el titulo: ").strip()
    if not termino:
        print("Aviso: No has introducido ningun termino.")
        return

    encontrados = [l for l in libros.values() if termino.lower() in l.titulo.lower()]

    if not encontrados:
        print(f"No existe ningun libro con '{termino}' en el titulo.\n")
        return

    print(f"\n--- RESULTADOS PARA '{termino}' ---")
    imprimir_cabecera_libros()
    for libro in encontrados:
        imprimir_fila_libro(libro)
    print("=" * 75)
    print(f"Se han encontrado {len(encontrados)} libro(s).\n")


# =====================================================================
# FUNCIONES DE PRESTAMOS Y DEVOLUCIONES
# =====================================================================

# Opcion 4: Prestar libro a un socio
def prestar_libro():
    print("\n--- PRESTAR LIBRO ---")
    cod_libro = input("Codigo del libro: ").strip().upper()
    cod_socio = input("Codigo del socio: ").strip().upper()

    try:
        # Comprobamos que el libro exista
        if cod_libro not in libros:
            raise LibroNoEncontradoError(cod_libro)

        # Comprobamos que el socio exista
        if cod_socio not in socios:
            raise SocioNoEncontradoError(cod_socio)

        libro = libros[cod_libro]
        socio = socios[cod_socio]

        # Comprobamos si el libro ya esta prestado
        if not libro.esta_disponible():
            raise LibroNoDisponibleError(cod_libro, libro.codigo_socio)

        # Comprobamos si el socio ya tiene un libro
        if socio.tiene_libro_prestado():
            raise SocioConLibroError(cod_socio, socio.codigo_libro)

        # Realizamos el prestamo
        libro.codigo_socio = cod_socio
        socio.codigo_libro = cod_libro

        print(f"\nPrestamo realizado: '{libro.titulo}' prestado a {socio.nombre}\n")

        # Guardamos en el log
        registrar_log(
            "PRESTAMO",
            f"Libro '{cod_libro}' ({libro.titulo}) prestado a socio '{cod_socio}' ({socio.nombre})"
        )

    # Capturamos nuestra excepcion personalizada usando sus atributos de instancia
    except ErrorBiblioteca as e:
        print(f"\nError [{e.codigo}]: {e.mensaje}")
        if e.detalle:
            print(f"Detalle: {e.detalle}")
        print()
        registrar_log("ERROR_PRESTAMO", f"[{e.codigo}] {e.mensaje}")


# Opcion 5: Devolver el libro de un socio
def devolver_libro():
    print("\n--- DEVOLVER LIBRO ---")
    cod_socio = input("Codigo del socio: ").strip().upper()

    try:
        if cod_socio not in socios:
            raise SocioNoEncontradoError(cod_socio)

        socio = socios[cod_socio]

        if not socio.tiene_libro_prestado():
            raise SocioSinLibroError(cod_socio)

        cod_libro = socio.codigo_libro
        libro = libros.get(cod_libro)

        # Liberamos el libro en el socio y en el libro
        socio.codigo_libro = None
        if libro:
            libro.codigo_socio = None
            titulo_libro = libro.titulo
        else:
            titulo_libro = cod_libro

        print(f"\nDevolucion realizada: '{titulo_libro}' devuelto por {socio.nombre}\n")

        registrar_log(
            "DEVOLUCION",
            f"Socio '{cod_socio}' ({socio.nombre}) devolvio el libro '{cod_libro}' ({titulo_libro})"
        )

    except ErrorBiblioteca as e:
        print(f"\nError [{e.codigo}]: {e.mensaje}")
        if e.detalle:
            print(f"Detalle: {e.detalle}")
        print()
        registrar_log("ERROR_DEVOLUCION", f"[{e.codigo}] {e.mensaje}")


# Opcion 6: Mostrar socios con libros prestados
def mostrar_socios_con_libros():
    socios_con_libro = [s for s in socios.values() if s.tiene_libro_prestado()]

    print("\n--- SOCIOS CON LIBROS PRESTADOS ---")
    if not socios_con_libro:
        print("Ningun socio tiene libros prestados actualmente.\n")
        return

    print(f"{'COD.':<6} {'NOMBRE':<28} {'COD. LIBRO':<12} {'TITULO'}")
    print("-" * 75)
    for socio in socios_con_libro:
        libro = libros.get(socio.codigo_libro)
        titulo = libro.titulo if libro else "(no encontrado)"
        titulo_corto = (titulo[:30] + "...") if len(titulo) > 33 else titulo
        print(f"{socio.codigo:<6} {socio.nombre:<28} {socio.codigo_libro:<12} {titulo_corto}")
    print("=" * 75)
    print(f"Total: {len(socios_con_libro)} socio(s) con prestamo activo\n")


# =====================================================================
# FUNCIONES PARA ANADIR SOCIOS Y LIBROS
# =====================================================================

# Opcion 7a: Anadir nuevo socio
def aniadir_socio():
    print("\n--- ANADIR SOCIO ---")
    codigo = input("Codigo del socio (ej: S016): ").strip().upper()
    nombre = input("Nombre completo: ").strip()
    email  = input("Email: ").strip()

    try:
        if codigo in socios:
            raise CodigoDuplicadoError("socio", codigo)

        nuevo_socio = Socio(codigo, nombre, email)
        socios[codigo] = nuevo_socio
        print(f"\nSocio '{nombre}' ({codigo}) anadido correctamente.\n")
        registrar_log("NUEVO_SOCIO", f"Socio '{codigo}' ({nombre}, {email}) anadido.")

    except CodigoDuplicadoError as e:
        print(f"\nError [{e.codigo}]: {e.mensaje}")
        print(f"Detalle: {e.detalle}\n")


# Opcion 7b: Anadir nuevo libro
def aniadir_libro():
    print("\n--- ANADIR LIBRO ---")
    codigo    = input("Codigo del libro (ej: L101): ").strip().upper()
    titulo    = input("Titulo: ").strip()
    autor     = input("Autor: ").strip()
    anio_str  = input("Anyo de publicacion: ").strip()
    categoria = input("Categoria: ").strip()

    try:
        if codigo in libros:
            raise CodigoDuplicadoError("libro", codigo)

        try:
            anio = int(anio_str)
        except ValueError:
            print(f"\nError: El anyo '{anio_str}' no es valido.\n")
            return

        nuevo_libro = Libro(codigo, titulo, autor, anio, categoria)
        libros[codigo] = nuevo_libro
        print(f"\nLibro '{titulo}' ({codigo}) anadido correctamente.\n")
        registrar_log("NUEVO_LIBRO", f"Libro '{codigo}' ({titulo}, {autor}, {anio}) anadido.")

    except CodigoDuplicadoError as e:
        print(f"\nError [{e.codigo}]: {e.mensaje}")
        print(f"Detalle: {e.detalle}\n")


def menu_aniadir():
    print("\n--- ANADIR ---")
    print("  1. Anadir socio")
    print("  2. Anadir libro")
    opcion = input("Elige una opcion (1 o 2): ").strip()

    if opcion == "1":
        aniadir_socio()
    elif opcion == "2":
        aniadir_libro()
    else:
        print("Opcion no valida.\n")


# =====================================================================
# MENU PRINCIPAL CICLICO
# =====================================================================

MENU_TEXTO = """
========================================
    SISTEMA DE GESTION DE BIBLIOTECA
========================================
  1. Mostrar todos los libros
  2. Mostrar libros disponibles
  3. Buscar libro por titulo
  4. Prestar un libro a un socio
  5. Devolver libro de un socio
  6. Mostrar socios con libros prestados
  7. Anadir socios y libros
  8. Salir y guardar datos
========================================
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

def ejecutar_menu():
    # Bucle ciclico hasta que el usuario elija la opcion 8
    while True:
        print(MENU_TEXTO)
        opcion = input("Elige una opcion (1-8): ").strip()

        if opcion == "8":
            guardar_todo()
            print("\nHasta pronto!\n")
            break
        elif opcion in OPCIONES:
            OPCIONES[opcion]()
        else:
            print("\nOpcion no valida. Introduce un numero del 1 al 8.\n")


# =====================================================================
# INICIO DEL PROGRAMA
# =====================================================================

def main():
    print("\n" + "=" * 50)
    print("   INICIANDO BIBLIOTECA")
    print("=" * 50)
    
    # Cargar datos iniciales
    cargar_libros()
    cargar_socios()
    print("=" * 50)
    
    registrar_log("INICIO", "El sistema de biblioteca se ha iniciado.")
    ejecutar_menu()


if __name__ == "__main__":
    main()
