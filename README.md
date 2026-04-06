# Proyecto_Ciencias1

Gestor de Base de Datos No Relacional en escritorio, implementado en Python con Tkinter, índice AVL y persistencia en archivo JSON.

## Objetivo

Este proyecto permite almacenar, consultar, actualizar y eliminar objetos JSON mediante una clave principal única (`id`).
La indexación se realiza con un árbol AVL para mantener eficiencia en operaciones por clave.

## Características

- Persistencia en archivo de texto plano JSON: `data/database.json`.
- Clave principal única por registro: `id`.
- Índice autobalanceado AVL:
	- Inserción en $O(\log n)$.
	- Búsqueda por clave en $O(\log n)$.
	- Actualización por clave en $O(\log n)$.
	- Eliminación por clave en $O(\log n)$.
- Consulta por criterios no clave (búsqueda lineal):
	- Contiene.
	- Igual a.
- Interfaz gráfica de escritorio con Tkinter.

## Estructura del proyecto

```text
.
├── data/
│   └── database.json
├── src/
│   ├── __init__.py
│   ├── avl_tree.py
│   ├── db_manager.py
│   ├── json_store.py
│   └── ui.py
├── main.py
└── README.md
```

## Requisitos

- Python 3.10+ (recomendado).
- Tkinter (normalmente incluido en instalaciones estándar de Python).

## Ejecución

Desde la raíz del proyecto:

```bash
python3 main.py
```

## Uso básico

1. Escribe el `ID` del registro.
2. En "Objeto JSON" ingresa un objeto JSON, por ejemplo:

```json
{
	"id": "101",
	"nombre": "Ana",
	"carrera": "Ingenieria",
	"semestre": 5
}
```

3. Usa los botones:
- `Guardar`: inserta registro nuevo.
- `Buscar por ID`: recupera por clave principal.
- `Actualizar`: reemplaza el objeto del ID indicado.
- `Eliminar`: borra el registro por ID.
- `Limpiar`: limpia formulario y muestra todos.

4. Para consultas no clave:
- Define `Campo` y `Valor`.
- Selecciona `Contiene` o `Igual a`.
- Pulsa `Consultar`.

## Notas técnicas

- El sistema reconstruye el árbol AVL al iniciar leyendo `data/database.json`.
- Después de cada operación de escritura (guardar, actualizar, eliminar), se persiste el estado completo.
- Se genera un backup automático `data/database.bak` cuando ya existe un archivo previo.

## Posibles mejoras

- Validaciones por esquema JSON.
- Consultas avanzadas con operadores numéricos.
- Exportación/importación de colecciones.
- Pruebas unitarias para AVL y gestor.