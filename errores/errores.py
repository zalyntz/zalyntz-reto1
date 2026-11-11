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
