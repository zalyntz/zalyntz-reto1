"""
modelos.py - Clases del dominio: Libro y Socio
"""

from __future__ import annotations


# ===========================================================================
# Clase Libro
# ===========================================================================

class Libro:
    """
    Representa un libro de la biblioteca.

    Atributos:
        codigo        (str)       : Identificador único del libro.
        titulo        (str)       : Título del libro.
        autor         (str)       : Autor del libro.
        anio          (int)       : Año de publicación.
        categoria     (str)       : Categoría o género literario.
        codigo_socio  (str|None)  : Código del socio que lo tiene prestado,
                                    o None si está disponible.
    """

    def __init__(
        self,
        codigo: str,
        titulo: str,
        autor: str,
        anio: int,
        categoria: str,
        codigo_socio: str | None = None
    ) -> None:
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = int(anio)
        self.categoria = categoria
        self.codigo_socio = codigo_socio  # None → disponible

    # -----------------------------------------------------------------------
    # Método personalizado
    # -----------------------------------------------------------------------

    def esta_disponible(self) -> bool:
        """Devuelve True si el libro no está prestado a ningún socio."""
        return self.codigo_socio is None

    def resumen_corto(self) -> str:
        """
        Devuelve una cadena de una línea con los datos más relevantes del libro.
        Método personalizado útil para listados.
        """
        estado = "Disponible" if self.esta_disponible() else f"Prestado → {self.codigo_socio}"
        return (
            f"[{self.codigo}] {self.titulo} | {self.autor} "
            f"({self.anio}) | {self.categoria} | {estado}"
        )

    # -----------------------------------------------------------------------
    # Serialización / deserialización
    # -----------------------------------------------------------------------

    def a_linea_txt(self) -> str:
        """Serializa el libro a una línea de texto separada por '|'."""
        socio = self.codigo_socio if self.codigo_socio else "NONE"
        return f"{self.codigo}|{self.titulo}|{self.autor}|{self.anio}|{self.categoria}|{socio}"

    @classmethod
    def desde_linea_txt(cls, linea: str) -> "Libro":
        """
        Crea un Libro a partir de una línea de texto del fichero.

        Formato esperado:
            codigo|titulo|autor|anio|categoria|codigo_socio
        """
        partes = linea.strip().split("|")
        codigo_socio = None if partes[5].upper() == "NONE" else partes[5]
        return cls(
            codigo=partes[0],
            titulo=partes[1],
            autor=partes[2],
            anio=int(partes[3]),
            categoria=partes[4],
            codigo_socio=codigo_socio
        )

    # -----------------------------------------------------------------------
    # Representación
    # -----------------------------------------------------------------------

    def __str__(self) -> str:
        return self.resumen_corto()

    def __repr__(self) -> str:
        return f"Libro(codigo={self.codigo!r}, titulo={self.titulo!r})"


# ===========================================================================
# Clase Socio
# ===========================================================================

class Socio:
    """
    Representa un socio de la biblioteca.

    Atributos:
        codigo        (str)       : Identificador único del socio.
        nombre        (str)       : Nombre completo.
        email         (str)       : Correo electrónico.
        codigo_libro  (str|None)  : Código del libro que tiene en préstamo,
                                    o None si no tiene ninguno.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        email: str,
        codigo_libro: str | None = None
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.email = email
        self.codigo_libro = codigo_libro  # None → sin préstamo

    # -----------------------------------------------------------------------
    # Método personalizado
    # -----------------------------------------------------------------------

    def tiene_libro_prestado(self) -> bool:
        """Devuelve True si el socio tiene algún libro en préstamo."""
        return self.codigo_libro is not None

    def ficha_socio(self) -> str:
        """
        Devuelve una cadena formateada con los datos del socio.
        Método personalizado útil para mostrar información detallada.
        """
        libro_info = self.codigo_libro if self.tiene_libro_prestado() else "Ninguno"
        return (
            f"Socio  : [{self.codigo}] {self.nombre}\n"
            f"Email  : {self.email}\n"
            f"Libro  : {libro_info}"
        )

    # -----------------------------------------------------------------------
    # Serialización / deserialización
    # -----------------------------------------------------------------------

    def a_linea_txt(self) -> str:
        """Serializa el socio a una línea de texto separada por '|'."""
        libro = self.codigo_libro if self.codigo_libro else "NONE"
        return f"{self.codigo}|{self.nombre}|{self.email}|{libro}"

    @classmethod
    def desde_linea_txt(cls, linea: str) -> "Socio":
        """
        Crea un Socio a partir de una línea de texto del fichero.

        Formato esperado:
            codigo|nombre|email|codigo_libro
        """
        partes = linea.strip().split("|")
        codigo_libro = None if partes[3].upper() == "NONE" else partes[3]
        return cls(
            codigo=partes[0],
            nombre=partes[1],
            email=partes[2],
            codigo_libro=codigo_libro
        )

    # -----------------------------------------------------------------------
    # Representación
    # -----------------------------------------------------------------------

    def __str__(self) -> str:
        return self.ficha_socio()

    def __repr__(self) -> str:
        return f"Socio(codigo={self.codigo!r}, nombre={self.nombre!r})"
