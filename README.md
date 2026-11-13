# Sistema de Gestión de Biblioteca

Proyecto final de Programación — Sistema de gestión de biblioteca desarrollado en Python con Programación Orientada a Objetos.

##  Estructura del proyecto

proyecto/
├── datos/
│   ├── libros.txt       # 100 libros (generado por IA)
│   └── socios.txt       # 15 socios (generado por IA)
├── errores/
│   ├── __init__.py
│   └── errores.py       # Excepciones personalizadas
├── modelo/
│   ├── __init__.py
│   └── modelos.py       # Clases Libro y Socio
├── log.txt              # Generado automáticamente al ejecutar
├── main.py              # Punto de entrada y menú principal
└── README.md
```

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
