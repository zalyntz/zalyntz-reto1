# Sistema de Gestión de Biblioteca

Aplicación de consola en Python para gestionar libros, socios y préstamos de una biblioteca.

## Ejecución

```bash
cd biblioteca
python main.py
```

## Estructura

```
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
```

## Funcionalidades

Menú cíclico con las siguientes opciones:

1. Mostrar todos los libros (tabla)
2. Mostrar libros disponibles
3. Buscar libros por título (sin distinguir mayúsculas)
4. Prestar un libro a un socio
5. Devolver un libro
6. Mostrar socios con libros prestados
7. Añadir socios o libros
8. Guardar y salir


## Posibles mejoras

- Migrar a base de datos (SQLite)
- Varios préstamos por socio
- Fechas límite y penalizaciones
- Sistema de reservas
- Búsqueda por autor, categoría o año
- Historial de préstamos
- Exportar informes a CSV o PDF
- Usuarios con contraseña
- Interfaz gráfica (Tkinter o Flask)
