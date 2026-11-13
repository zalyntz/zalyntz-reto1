# -*- coding: utf-8 -*-
"""
Modulo de errores: excepciones personalizadas para el sistema de biblioteca.
"""

# Excepcion base que hereda de Exception con atributos de instancia propios
class ErrorBiblioteca(Exception):
    def __init__(self, mensaje, codigo, detalle=""):
        super().__init__(mensaje)
        self.mensaje = mensaje    # Mensaje de error
        self.codigo = codigo      # Codigo identificador del error
        self.detalle = detalle    # Detalle adicional

    def __str__(self):
        texto = f"[{self.codigo}] {self.mensaje}"
        if self.detalle:
            texto += f" - Detalle: {self.detalle}"
        return texto


# Error cuando un libro ya esta prestado
class LibroNoDisponibleError(ErrorBiblioteca):
    def __init__(self, codigo_libro, codigo_socio_actual):
        super().__init__(
            mensaje=f"El libro '{codigo_libro}' ya esta prestado.",
            codigo="LIBRO_NO_DISPONIBLE",
            detalle=f"Lo tiene prestado el socio '{codigo_socio_actual}'."
        )


# Error cuando un socio ya tiene un libro y pide otro
class SocioConLibroError(ErrorBiblioteca):
    def __init__(self, codigo_socio, codigo_libro_actual):
        super().__init__(
            mensaje=f"El socio '{codigo_socio}' ya tiene un libro en prestamo.",
            codigo="SOCIO_CON_LIBRO",
            detalle=f"Tiene que devolver antes el libro '{codigo_libro_actual}'."
        )


# Error si no se encuentra el libro
class LibroNoEncontradoError(ErrorBiblioteca):
    def __init__(self, codigo_libro):
        super().__init__(
            mensaje=f"No se ha encontrado ningun libro con codigo '{codigo_libro}'.",
            codigo="LIBRO_NO_ENCONTRADO"
        )


# Error si no se encuentra el socio
class SocioNoEncontradoError(ErrorBiblioteca):
    def __init__(self, codigo_socio):
        super().__init__(
            mensaje=f"No se ha encontrado ningun socio con codigo '{codigo_socio}'.",
            codigo="SOCIO_NO_ENCONTRADO"
        )


# Error al intentar devolver si el socio no tiene libro
class SocioSinLibroError(ErrorBiblioteca):
    def __init__(self, codigo_socio):
        super().__init__(
            mensaje=f"El socio '{codigo_socio}' no tiene ningun libro para devolver.",
            codigo="SOCIO_SIN_LIBRO"
        )


# Error al intentar anadir codigo que ya existe
class CodigoDuplicadoError(ErrorBiblioteca):
    def __init__(self, tipo, codigo):
        super().__init__(
            mensaje=f"Ya existe un {tipo} con el codigo '{codigo}'.",
            codigo="CODIGO_DUPLICADO",
            detalle="Introduce un codigo que no este en uso."
=======
"""
errores.py - Excepciones personalizadas del Sistema de Gestión de Biblioteca
"""


class ErrorBiblioteca(Exception):
    """
    Excepción base personalizada para errores del sistema de biblioteca.
    
    Atributos de instancia:
        mensaje  -- descripción del error
        codigo   -- código identificador del error
        detalle  -- información adicional sobre el contexto del error
    """

    def __init__(self, mensaje: str, codigo: str, detalle: str = ""):
        """
        Inicializa la excepción con mensaje, código y detalle opcional.

        Args:
            mensaje (str): Descripción legible del error.
            codigo  (str): Código corto identificador (ej. 'LIBRO_NO_DISP').
            detalle (str): Contexto adicional (opcional).
        """
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo
        self.detalle = detalle

    def __str__(self) -> str:
        """Representación legible de la excepción."""
        base = f"[{self.codigo}] {self.mensaje}"
        if self.detalle:
            base += f" — Detalle: {self.detalle}"
        return base


# ---------------------------------------------------------------------------
# Excepciones específicas (heredan de ErrorBiblioteca)
# ---------------------------------------------------------------------------

class LibroNoDisponibleError(ErrorBiblioteca):
    """Se lanza cuando se intenta prestar un libro que ya está prestado."""

    def __init__(self, codigo_libro: str, codigo_socio_actual: str):
        super().__init__(
            mensaje=f"El libro '{codigo_libro}' no está disponible.",
            codigo="LIBRO_NO_DISP",
            detalle=f"Actualmente prestado al socio '{codigo_socio_actual}'."
        )


class SocioConLibroError(ErrorBiblioteca):
    """Se lanza cuando un socio ya tiene un libro prestado y pide otro."""

    def __init__(self, codigo_socio: str, codigo_libro_actual: str):
        super().__init__(
            mensaje=f"El socio '{codigo_socio}' ya tiene un libro prestado.",
            codigo="SOCIO_CON_LIBRO",
            detalle=f"Libro en préstamo: '{codigo_libro_actual}'."
        )


class LibroNoEncontradoError(ErrorBiblioteca):
    """Se lanza cuando no se encuentra un libro por su código."""

    def __init__(self, codigo_libro: str):
        super().__init__(
            mensaje=f"No se encontró ningún libro con código '{codigo_libro}'.",
            codigo="LIBRO_NO_ENCONTRADO",
            detalle=""
        )


class SocioNoEncontradoError(ErrorBiblioteca):
    """Se lanza cuando no se encuentra un socio por su código."""

    def __init__(self, codigo_socio: str):
        super().__init__(
            mensaje=f"No se encontró ningún socio con código '{codigo_socio}'.",
            codigo="SOCIO_NO_ENCONTRADO",
            detalle=""
        )


class SocioSinLibroError(ErrorBiblioteca):
    """Se lanza cuando se intenta devolver un libro a un socio que no tiene ninguno."""

    def __init__(self, codigo_socio: str):
        super().__init__(
            mensaje=f"El socio '{codigo_socio}' no tiene ningún libro en préstamo.",
            codigo="SOCIO_SIN_LIBRO",
            detalle=""
        )


class CodigoDuplicadoError(ErrorBiblioteca):
    """Se lanza cuando se intenta añadir un libro o socio con código ya existente."""

    def __init__(self, tipo: str, codigo: str):
        super().__init__(
            mensaje=f"Ya existe un {tipo} con el código '{codigo}'.",
            codigo="CODIGO_DUPLICADO",
            detalle=f"Tipo: {tipo}."

        )
