Sistema de Gestión de Biblioteca

Aplicación de consola en Python para gestionar libros, socios y préstamos de una biblioteca.

Ejecución
bash
cd biblioteca
python main.py
Estructura
biblioteca/
├── datos/
│   ├── libros.txt       # 100 libros
│   └── socios.txt       # 15 socios
├── errores/
│   └── errores.py       # Excepciones personalizadas
├── modelo/
│   └── modelos.py       # Clases Libro y Socio
├── log.txt              # Registro de eventos
├── main.py              # Menú y lógica del sistema
└── README.md
Funcionalidades

Menú cíclico con las siguientes opciones:

Mostrar todos los libros (tabla)
Mostrar libros disponibles
Buscar libros por título (sin distinguir mayúsculas)
Prestar un libro a un socio
Devolver un libro
Mostrar socios con libros prestados
Añadir socios o libros
Guardar y salir
Diseño
Modelo (modelo/modelos.py)
Clase	Atributos	Métodos principales
Libro	codigo, titulo, autor, anio, categoria, codigo_socio	esta_disponible(), resumen_corto()
Socio	codigo, nombre, email, codigo_libro	tiene_libro_prestado(), ficha_socio()

Ambas clases incluyen a_linea_txt() y desde_linea_txt() para la persistencia.

Excepciones (errores/errores.py)

ErrorBiblioteca es la clase base (atributos mensaje, codigo, detalle). De ella derivan:

LibroNoDisponibleError: el libro ya está prestado
SocioConLibroError: el socio ya tiene un préstamo
LibroNoEncontradoError: el libro no existe
SocioNoEncontradoError: el socio no existe
SocioSinLibroError: el socio no tiene libro que devolver
CodigoDuplicadoError: el código ya existe
Persistencia y log

Al arrancar se cargan los datos de datos/; la opción 8 guarda el estado actual.

Fichero	Formato por línea
libros.txt	CODIGO|TITULO|AUTOR|AÑO|CATEGORIA|COD_SOCIO_O_NONE
socios.txt	CODIGO|NOMBRE|EMAIL|COD_LIBRO_O_NONE
log.txt	[FECHA][EVENTO][DETALLE]

Se registran arranques, préstamos, devoluciones, altas y errores.

Posibles mejoras
Migrar a base de datos (SQLite)
Varios préstamos por socio
Fechas límite y penalizaciones
Sistema de reservas
Búsqueda por autor, categoría o año
Historial de préstamos
Exportar informes a CSV o PDF
Usuarios con contraseña
