# -*- coding: utf-8 -*-
"""
main.py - Sistema de Gestion de Biblioteca
Punto de entrada de la aplicacion.
"""

import os
import sys

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
