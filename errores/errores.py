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
        )
