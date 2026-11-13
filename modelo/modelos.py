# -*- coding: utf-8 -*-
"""
Modulo de modelos: define las clases de la biblioteca.
"""

class Libro:
    """
    Clase que representa un libro en la biblioteca.
    """
    def __init__(self, codigo, titulo, autor, anio, categoria, codigo_socio=None):
        self.codigo = codigo              # Codigo unico del libro (ej: L001)
        self.titulo = titulo              # Titulo del libro
        self.autor = autor                # Autor
        self.anio = int(anio)             # Anyo de publicacion
        self.categoria = categoria        # Categoria o genero
        self.codigo_socio = codigo_socio  # None si esta libre, o codigo del socio si esta prestado

    # Metodo personalizado: comprueba si el libro esta disponible para prestar
    def esta_disponible(self):
        return self.codigo_socio is None

    # Metodo personalizado: devuelve un resumen en una linea para mostrar en listas
    def resumen_corto(self):
        estado = "Disponible" if self.esta_disponible() else f"Prestado -> {self.codigo_socio}"
        return f"[{self.codigo}] {self.titulo} - {self.autor} ({self.anio}) | {self.categoria} | {estado}"

    # Convierte el libro a formato texto para guardarlo en el fichero
    def a_linea_txt(self):
        socio = self.codigo_socio if self.codigo_socio else "NONE"
        return f"{self.codigo}|{self.titulo}|{self.autor}|{self.anio}|{self.categoria}|{socio}"

    # Crea un libro a partir de una linea del fichero
    @classmethod
    def desde_linea_txt(cls, linea):
        partes = linea.strip().split("|")
        cod_socio = None if partes[5].upper() == "NONE" else partes[5]
        return cls(partes[0], partes[1], partes[2], int(partes[3]), partes[4], cod_socio)

    def __str__(self):
        return self.resumen_corto()
