
# Sistema de Gestion de Biblioteca

Proyecto final de Programacion (DAM). Sistema de gestion de una biblioteca por consola desarrollado en Python con Programacion Orientada a Objetos, funciones modulares, persistencia en ficheros de texto y manejo de excepciones personalizadas.

## Como ejecutar el proyecto

1. Abrir una terminal en la carpeta del proyecto:
   ```bash
   cd biblioteca
   ```
2. Ejecutar el fichero principal:
   ```bash
   python main.py
   ```

## Estructura del proyecto

```
proyecto/
├── datos/
│   ├── libros.txt       # Fichero con 100 libros
│   └── socios.txt       # Fichero con 15 socios
├── errores/
│   ├── __init__.py
│   └── errores.py       # Excepciones personalizadas
├── modelo/
│   ├── __init__.py
│   └── modelos.py       # Clases Libro y Socio
├── log.txt              # Registro de eventos
├── main.py              # Menu y funciones del sistema
└── README.md            # Documentacion
```

## Requisitos implementados

### 1. Clases del modelo (modelo/modelos.py)
* **Libro**: Contiene los atributos `codigo`, `titulo`, `autor`, `anio`, `categoria` y `codigo_socio` (None si esta disponible).
  * Metodo personalizado `esta_disponible()`: Comprueba si el libro esta libre.
  * Metodo personalizado `resumen_corto()`: Devuelve los datos del libro en una linea legible.
  * Metodos `a_linea_txt()` y `desde_linea_txt()` para persistencia.
* **Socio**: Contiene los atributos `codigo`, `nombre`, `email` y `codigo_libro` (None si no tiene libro).
  * Metodo personalizado `tiene_libro_prestado()`: Comprueba si tiene un prestamo activo.
  * Metodo personalizado `ficha_socio()`: Muestra los datos del socio.
  * Metodos `a_linea_txt()` y `desde_linea_txt()` para persistencia.

### 2. Excepciones personalizadas (errores/errores.py)
* Clase base `ErrorBiblioteca` que hereda de `Exception` con atributos de instancia propios: `mensaje`, `codigo` y `detalle`.
* Excepciones derivadas:
  * `LibroNoDisponibleError`: Si el libro ya esta prestado a otro socio.
  * `SocioConLibroError`: Si el socio ya tiene un libro en prestamo.
  * `LibroNoEncontradoError`: Si no existe el libro indicado.
  * `SocioNoEncontradoError`: Si no existe el socio indicado.
  * `SocioSinLibroError`: Si el socio no tiene ningun libro para devolver.
  * `CodigoDuplicadoError`: Si se intenta anadir un codigo ya existente.
* En `main.py` los bloques `try/except` capturan `ErrorBiblioteca` y acceden a los atributos de instancia `e.codigo` y `e.detalle`.

### 3. Ficheros y persistencia
* Al arrancar el programa se cargan los 100 libros de `datos/libros.txt` y los 15 socios de `datos/socios.txt`.
* Se muestra el mensaje obligatorio confirmando la carga de los libros.
* Con la opcion 8 del menu se vuelca el estado actual a los ficheros.

### 4. Log de actividad (log.txt)
* Se registran eventos importantes (arranque, prestamos, devoluciones, altas y errores) con el formato exacto:
  `[Fecha][nombre del evento][detalles]`

### 5. Menu principal
* Menu ciclico con opciones del 1 al 8 mediante un bucle while:
  1. Mostrar todos los libros en formato tabla.
  2. Mostrar libros disponibles.
  3. Buscar libros por cualquier termino del titulo (sin distinguir mayusculas/minusculas).
  4. Prestar libro a un socio con control de errores.
  5. Devolver libro de un socio.
  6. Mostrar socios que tienen libros prestados.
  7. Anadir nuevos socios o libros.
  8. Salir y guardar los datos.

## Posibles mejoras de la aplicacion

1. **Base de datos relacional**: Usar SQLite en lugar de ficheros de texto para mejorar la integridad de los datos.
2. **Varios prestamos por socio**: Permitir que un socio pueda tener mas de un libro a la vez (por ejemplo un maximo de 3).
3. **Control de fechas y penalizaciones**: Anadir fecha limite de devolucion y penalizaciones a los socios que entreguen tarde.
4. **Sistema de reservas**: Permitir que un socio reserve un libro que ya este prestado a otro usuario.
5. **Busqueda avanzada**: Poder buscar por autor, categoria o anio ademas de por titulo.
6. **Interfaz grafica**: Desarrollar una interfaz visual con Tkinter o una aplicacion web con Flask.
=======
# Sistema de Gestión de Biblioteca

Proyecto final de Programación — Sistema de gestión de biblioteca desarrollado en Python con Programación Orientada a Objetos.

## Mi Menu

| Opción | Descripción |
|--------|-------------|
| 1 | Ver todos los libros en formato tabla |
| 2 | Ver sólo los libros disponibles |
| 3 | Buscar libro por término en el título |
| 4 | Prestar libro a un socio |
| 5 | Devolver el libro de un socio |
| 6 | Ver socios con préstamos activos |
| 7 | Añadir nuevo socio o libro |
| 8 | Salir y guardar todos los datos |

## Formato de los ficheros

**libros.txt** — cada línea: `CODIGO|TITULO|AUTOR|AÑO|CATEGORIA|COD_SOCIO_O_NONE`

**socios.txt** — cada línea: `CODIGO|NOMBRE|EMAIL|COD_LIBRO_O_NONE`

**log.txt** — cada línea: `[FECHA][EVENTO][DETALLE]`

## Diseño orientado a objetos

### Clase `Libro` (modelo/modelos.py)
- Atributos: `codigo`, `titulo`, `autor`, `anio`, `categoria`, `codigo_socio`
- Método personalizado: `esta_disponible()` → bool
- Método personalizado: `resumen_corto()` → str 
- Serialización: `a_linea_txt()` / `desde_linea_txt()`

### Clase `Socio` (modelo/modelos.py)
- Atributos: `codigo`, `nombre`, `email`, `codigo_libro`
- Método personalizado: `tiene_libro_prestado()` → bool
- Método personalizado: `ficha_socio()` → str (ficha detallada del socio)
- Serialización: `a_linea_txt()` / `desde_linea_txt()`

### Excepciones personalizadas (errores/errores.py)
- `ErrorBiblioteca` — base con atributos `mensaje`, `codigo`, `detalle`
- `LibroNoDisponibleError` — libro ya prestado
- `SocioConLibroError` — socio ya tiene un préstamo
- `LibroNoEncontradoError` — código de libro inexistente
- `SocioNoEncontradoError` — código de socio inexistente
- `SocioSinLibroError` — socio no tiene libro para devolver
- `CodigoDuplicadoError` — intento de añadir código ya existente

## Posibles mejoras

- **Base de datos**: Migrar el almacenamiento de ficheros `.txt` a SQL.
- **Múltiples préstamos**: Permitir que un socio tenga más de un libro prestado .
- **Fechas de préstamo y devolución**: Registrar cuándo se prestó un libro .
- **Sistema de reservas**: Que un socio pueda reservar un libro actualmente prestado.
- **Búsqueda avanzada**: Buscar por autor, categoría, año,.
- **Exportar a CSV o PDF**: Generar informes en diferentes formatos.
- **Sistema de usuarios con contraseña**
- **Categorías y etiquetas**: Mejorar la clasificación con múltiples categorías por libro.
- **Historial de préstamos**: Mantener un registro histórico completo de todos los préstamos.


