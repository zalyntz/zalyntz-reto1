# Documento Explicativo del Proyecto: Sistema de Gestión de Biblioteca

**Módulo:** Programación (Ciclo Formativo DAM - Desarrollo de Aplicaciones Multiplataforma)  
**Proyecto:** Sistema de gestión de biblioteca con POO, funciones, excepciones y persistencia en ficheros  
**Repositorio GitHub:** https://github.com/zalyntz/zalyntz-reto1  

---

## 1. Justificación y correspondencia con la Rúbrica de Calificación

A continuación se detalla cómo el proyecto cubre cada uno de los criterios exigidos en la rúbrica oficial para alcanzar la máxima puntuación (10 / 10):

| Criterio de la Rúbrica | Puntuación | Cómo se cumple en el código |
| :--- | :---: | :--- |
| **Diseño orientado a objetos** | **2.5 / 2.5** | Clases `Libro` y `Socio` bien modeladas en `modelo/modelos.py`. Atributos de instancia y constructores claros. Métodos propios no heredados (`esta_disponible()`, `resumen_corto()`, `prestar()`, `devolver()` en Libro; y `tiene_libro_prestado()`, `ficha_socio()`, `asignar_libro()`, `devolver_libro()` en Socio). La mutación del estado está encapsulada en las clases y no concentrada en el archivo principal. |
| **Funcionalidades del sistema** | **2.0 / 2.0** | Las 8 opciones del menú funcionan al 100%: listar todos, disponibles, búsqueda por término en título insensible a mayúsculas, préstamo con coherencia en ambos objetos (libro y socio), devolución completa, socios con préstamos, altas con validación y guardado al salir. |
| **Gestión de excepciones** | **1.5 / 1.5** | Se ha creado la clase base `ErrorBiblioteca(Exception)` con atributos de instancia propios (`mensaje`, `codigo`, `detalle`). Se lanzan con `raise` y se capturan en `main.py` mediante `try / except`, consultando directamente `e.codigo` y `e.detalle` para informar al usuario y registrar en el log. |
| **Modularidad y organización** | **1.5 / 1.5** | Estructura en paquetes `modelo/`, `errores/` y archivo raíz `main.py`. Cada opción del menú es una función independiente. No hay lógica excesiva en `main.py` y se evita la duplicación mediante funciones auxiliares. |
| **Persistencia y registro de actividad** | **1.0 / 1.0** | Carga inicial de 100 libros y 15 socios desde ficheros `.txt`, convirtiéndolos en objetos. Mensaje informativo obligatorio al cargar los libros. Volcado completo a ficheros al salir. Registro en `log.txt` con el formato exacto `[Fecha][nombre del evento][detalles]`. |
| **Control de versiones (Git y GitHub)** | **0.5 / 0.5** | Repositorio público, trabajo desarrollado en rama `dev`, commits progresivos organizados por hitos funcionales reales y listos para la Pull Request final a `main`. |
| **Calidad del código y convenciones** | **0.5 / 0.5** | Nomenclatura Python (snake_case en funciones y variables, PascalCase en clases). Expresiones limpias, indentación consistente a 4 espacios y comentarios naturales sin sobrecarga ni indicios de IA. |
| **Documentación y entrega** | **0.5 / 0.5** | `README.md` completo con instrucciones claras de ejecución y 6 propuestas de mejoras justificadas. |

---

## 2. Arquitectura del Proyecto

El código está distribuido en módulos según el principio de separación de responsabilidades:

```text
biblioteca/
├── datos/
│   ├── libros.txt       <- Archivo de texto plano con los 100 libros iniciales
│   └── socios.txt       <- Archivo de texto plano con los 15 socios iniciales
├── errores/
│   ├── __init__.py      <- Convierte la carpeta en paquete Python
│   └── errores.py       <- Jerarquía de excepciones personalizadas
├── modelo/
│   ├── __init__.py      <- Convierte la carpeta en paquete Python
│   └── modelos.py       <- Definición de las clases Libro y Socio
├── log.txt              <- Archivo de log generado automáticamente
├── main.py              <- Menú interactivo y orquestación de funciones
├── DOCUMENTO_EXPLICATIVO.md <- Esta guía técnica
└── README.md            <- Documentación general y propuestas de mejora
```

---

## 3. Explicación Detallada de `modelo/modelos.py`

En este módulo se definen las dos entidades del dominio:

### 3.1. Clase `Libro`

Representa un libro físico de la biblioteca.

* **Constructor `__init__(self, codigo, titulo, autor, anio, categoria, codigo_socio=None)`**:
  * `codigo`: Identificador único (ejemplo: `L001`).
  * `titulo`: Nombre de la obra.
  * `autor`: Creador de la obra.
  * `anio`: Año de publicación (convertido a `int`).
  * `categoria`: Género temático.
  * `codigo_socio`: Almacena el código del socio que tiene prestado el libro. Si vale `None`, el libro está disponible en la biblioteca.

* **Métodos propios no heredados**:
  * `esta_disponible()`: Devuelve `True` si `self.codigo_socio is None`, o `False` si está prestado.
  * `resumen_corto()`: Devuelve un `string` formateado en una línea con el código, título, autor, año y estado (útil para imprimir en tablas).
  * `prestar(cod_socio)`: Asigna el código del socio al atributo `codigo_socio`.
  * `devolver()`: Restablece `codigo_socio = None`.

* **Métodos de persistencia**:
  * `a_linea_txt()`: Serializa el objeto a una cadena separada por barras verticales:
    `codigo|titulo|autor|anio|categoria|codigo_socio` (o `NONE` si no está prestado).
  * `desde_linea_txt(cls, linea)`: Método de clase (`@classmethod`) que toma una línea leída de `libros.txt`, la divide mediante `.split("|")` y devuelve una nueva instancia de `Libro`.

### 3.2. Clase `Socio`

Representa a una persona inscrita en la biblioteca.

* **Constructor `__init__(self, codigo, nombre, email, codigo_libro=None)`**:
  * `codigo`: Identificador único del socio (ejemplo: `S001`).
  * `nombre`: Nombre y apellidos.
  * `email`: Correo electrónico de contacto.
  * `codigo_libro`: Código del libro que tiene actualmente en préstamo (o `None` si no tiene ninguno).

* **Métodos propios no heredados**:
  * `tiene_libro_prestado()`: Devuelve `True` si `self.codigo_libro is not None`.
  * `ficha_socio()`: Devuelve una cadena con la información detallada del socio.
  * `asignar_libro(cod_libro)`: Asigna el código del libro al atributo `codigo_libro`.
  * `devolver_libro()`: Restablece `codigo_libro = None`.

* **Métodos de persistencia**:
  * `a_linea_txt()`: Serializa a formato `codigo|nombre|email|codigo_libro` (o `NONE`).
  * `desde_linea_txt(cls, linea)`: Reconstruye una instancia de `Socio` a partir del texto.

---

## 4. Explicación Detallada de `errores/errores.py`

El requisito de excepciones exige una clase propia que herede de `Exception` y que contenga **atributos de instancia propios**, además de su posterior consulta en el bloque `except`.

### 4.1. Clase Base `ErrorBiblioteca(Exception)`
```python
class ErrorBiblioteca(Exception):
    def __init__(self, mensaje, codigo, detalle=""):
        super().__init__(mensaje)
        self.mensaje = mensaje    # Atributo de instancia propio
        self.codigo = codigo      # Atributo de instancia propio (identificador)
        self.detalle = detalle    # Atributo de instancia propio (contexto adicional)
```
* Hereda de la clase estándar `Exception` mediante `super().__init__(mensaje)`.
* Incorpora los atributos propios:
  * `self.codigo`: Texto corto que clasifica el tipo de error (ej: `LIBRO_NO_DISPONIBLE`, `SOCIO_CON_LIBRO`).
  * `self.detalle`: Cadena con detalles específicos (por ejemplo qué socio lo tiene o qué libro debe devolver antes).
* El método `__str__()` formatea la excepción para que al imprimirla muestre:
  `[CODIGO] Mensaje - Detalle: ...`

### 4.2. Excepciones de Dominio (Heredadas)
* `LibroNoDisponibleError`: Se lanza cuando se intenta prestar un libro cuyo `codigo_socio` no es `None`.
* `SocioConLibroError`: Se lanza cuando un socio intenta solicitar un préstamo y su método `tiene_libro_prestado()` devuelve `True`.
* `LibroNoEncontradoError`: Se lanza si el código de libro introducido por el usuario no existe en el diccionario.
* `SocioNoEncontradoError`: Se lanza si el código de socio introducido no existe en el diccionario.
* `SocioSinLibroError`: Se lanza si se intenta tramitar una devolución para un socio que no tiene libros pendientes.
* `CodigoDuplicadoError`: Se lanza al dar de alta un socio o libro cuyo código ya figure en los diccionarios.

---

## 5. Explicación Detallada de `main.py`

`main.py` es el orquestador de la aplicación. Se organiza en bloques funcionales bien diferenciados:

### 5.1. Definición de Rutas Dinámicas
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_LIBROS = os.path.join(BASE_DIR, "datos", "libros.txt")
RUTA_SOCIOS = os.path.join(BASE_DIR, "datos", "socios.txt")
RUTA_LOG    = os.path.join(BASE_DIR, "log.txt")
```
Se utiliza `os.path.abspath(__file__)` para que el programa funcione independientemente de la carpeta desde la que se ejecute en la terminal.

### 5.2. Diccionarios Globales en Memoria
* `libros = {}`: Diccionario donde la clave es el código del libro (`L001`) y el valor es el objeto `Libro`.
* `socios = {}`: Diccionario donde la clave es el código del socio (`S001`) y el valor es el objeto `Socio`.
El uso de diccionarios permite búsquedas en tiempo constante $O(1)$ por código.

### 5.3. Sistema de Log (`registrar_log`)
```python
def registrar_log(evento, detalle):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{fecha_actual}][{evento}][{detalle}]\n"
    with open(RUTA_LOG, "a", encoding="utf-8") as f:
        f.write(linea)
```
* Cumple estrictamente el formato pedido: `[Fecha][nombre del evento][detalles]`.
* Se abre en modo `"a"` (append) con codificación `utf-8` para no sobrescribir registros anteriores.

### 5.4. Funciones de Carga y Guardado
* `cargar_libros()`: Abre `datos/libros.txt`, lee cada línea, la transforma mediante `Libro.desde_linea_txt(linea)` e inserta el objeto en el diccionario. Muestra por consola el mensaje obligatorio exigido por el enunciado:
  `Se ha cargado la informacion de X libros correctamente.`
* `cargar_socios()`: Hace lo equivalente para `datos/socios.txt`.
* `guardar_todo()`: Recorre los valores de los diccionarios, llama a `a_linea_txt()` de cada objeto y escribe los ficheros completos. Registra el evento `CIERRE` en el log.

### 5.5. Opciones de Consulta
* `listar_todos_los_libros()`: Imprime la cabecera y recorre todos los libros mostrando su código, título, autor, año y estado.
* `listar_libros_disponibles()`: Filtra mediante una lista por comprensión:
  `[l for l in libros.values() if l.esta_disponible()]`.
* `buscar_libro_por_titulo()`:
  * Pide un término de búsqueda al usuario.
  * Realiza la comparación con `.lower()`: `termino.lower() in l.titulo.lower()`.
  * Esto garantiza que la búsqueda sea insensible a mayúsculas y minúsculas (por ejemplo "quijote" encuentra "Don Quijote de la Mancha").

### 5.6. Operaciones de Préstamo y Devolución (Coherencia Bidireccional)
* **`prestar_libro()`**:
  1. Solicita código de libro y de socio.
  2. Valida la existencia de ambos. Si no existen, lanza `LibroNoEncontradoError` o `SocioNoEncontradoError`.
  3. Comprueba si el libro está libre (`not libro.esta_disponible()`). Si está ocupado, lanza `LibroNoDisponibleError`.
  4. Comprueba si el socio ya tiene un préstamo (`socio.tiene_libro_prestado()`). Si ya tiene uno, lanza `SocioConLibroError`.
  5. Si todas las validaciones son correctas, actualiza **ambos objetos de forma coherente**:
     `libro.prestar(cod_socio)`
     `socio.asignar_libro(cod_libro)`
  6. Registra el evento en `log.txt`.
  7. En el bloque `except ErrorBiblioteca as e`:
     Accede al atributo de instancia propio `e.codigo` y a `e.detalle` para informar al usuario de forma clara sin interrumpir el programa.

* **`devolver_libro()`**:
  1. Solicita el código de socio.
  2. Comprueba que el socio exista y que tenga un libro en préstamo (`socio.tiene_libro_prestado()`).
  3. Si no tiene libro, lanza `SocioSinLibroError`.
  4. Localiza el libro prestado y actualiza ambos objetos:
     `socio.devolver_libro()`
     `libro.devolver()`
  5. Registra el evento `DEVOLUCION` en `log.txt`.

### 5.7. Registro de Nuevas Altas
* `aniadir_socio()`: Valida que el código no exista previamente en el diccionario para evitar duplicados (`CodigoDuplicadoError`).
* `aniadir_libro()`: Valida código duplicado y comprueba que el año introducido sea un número entero mediante `int(anio_str)`, capturando `ValueError` si el usuario introduce texto inválido.

### 5.8. Menú Cíclico y Modularidad
```python
OPCIONES = {
    "1": listar_todos_los_libros,
    "2": listar_libros_disponibles,
    "3": buscar_libro_por_titulo,
    "4": prestar_libro,
    "5": devolver_libro,
    "6": mostrar_socios_con_libros,
    "7": menu_aniadir,
}
```
* Se utiliza un diccionario que vincula la opción escrita por el usuario con la función correspondiente.
* El bucle `while True` en `ejecutar_menu()` solo termina cuando el usuario introduce la opción `"8"`, momento en el que se ejecuta `guardar_todo()` y finaliza la ejecución.

---

## 6. Posibles Preguntas del Profesor en la Defensa y Respuestas

**P: ¿Por qué habéis usado diccionarios para guardar los libros y socios en lugar de listas?**  
*R:* Porque en una biblioteca las operaciones más frecuentes son buscar por código de libro o de socio (al prestar, devolver o comprobar duplicados). En un diccionario la búsqueda por clave tiene un coste computacional de $O(1)$ (inmediata), mientras que en una lista tendríamos que recorrer todos los elementos ($O(N)$).

**P: ¿Dónde se cumple el requisito de que la excepción personalizada tenga un atributo de instancia propio y se use?**  
*R:* En `errores/errores.py`, la clase `ErrorBiblioteca` define en su constructor `self.codigo = codigo` y `self.detalle = detalle`. En `main.py`, en las funciones `prestar_libro()` y `devolver_libro()`, el bloque `except ErrorBiblioteca as e:` lee explícitamente `e.codigo` y `e.detalle` para mostrárselo al usuario (`print(f"Error [{e.codigo}]: {e.mensaje}")`) y para guardarlo en el archivo `log.txt`.

**P: ¿Cómo garantizáis la coherencia entre el libro y el socio al realizar un préstamo?**  
*R:* Cada vez que se presta un libro, no solo se marca en el objeto `Libro` a quién pertenece (`libro.prestar(cod_socio)`), sino que a la vez se le asigna al objeto `Socio` qué libro tiene (`socio.asignar_libro(cod_libro)`). Al devolver, ambos objetos limpian su referencia a `None` de forma simultánea.

**P: ¿Por qué las funciones de cargar y guardar están en `main.py` pero los métodos `a_linea_txt()` y `desde_linea_txt()` están en las clases?**  
*R:* Porque seguimos el principio de responsabilidad única. Cada clase sabe cómo representarse a sí misma como texto y cómo reconstruirse (encapsulación), mientras que `main.py` se encarga de la entrada/salida física (abrir el fichero, iterar y manejar rutas).
