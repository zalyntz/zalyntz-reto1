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
