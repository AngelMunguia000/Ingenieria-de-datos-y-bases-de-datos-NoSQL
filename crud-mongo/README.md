# Operaciones CRUD en MongoDB con Python

Práctica de la asignatura Optativa III: Ciencia de Datos, UNE Plantel Centro.

El script modela una colección documental de productos, ejecuta las cuatro operaciones CRUD y realiza una agregación por categoría.

**Autor:** Angel David Munguía Zúñiga

## Contenido del proyecto

| Archivo | Descripción |
|---|---|
| `crud_mongo.py` | Script con la conexión, las cuatro operaciones CRUD y la agregación |
| `requirements.txt` | Dependencias del proyecto |

## Requisitos e instalación

Se requiere Python 3.10 o superior.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python crud_mongo.py
```

## Conexión a MongoDB

La práctica utiliza la Opción B de la guía del curso: la librería `mongomock`, que simula un servidor MongoDB en memoria y expone la misma interfaz que `pymongo`, por lo que no requiere instalar ni configurar un servidor.

```python
import mongomock
client = mongomock.MongoClient()
```

Para ejecutar el script contra un servidor real basta con sustituir esas dos líneas; el resto del código no cambia.

```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")  # o la cadena de conexión de MongoDB Atlas
```

Una vez establecida la conexión, se selecciona la base de datos `tienda` y la colección `productos`. MongoDB crea ambas de forma automática al insertar el primer documento, sin necesidad de definir un esquema previo.

## Modelo de datos

Cada producto se almacena como un documento con estructura similar a JSON. Todos los documentos comparten los campos `nombre`, `categoria`, `precio` y `stock`, y cada uno puede incluir atributos propios.

```json
{
  "nombre": "Laptop",
  "categoria": "Computo",
  "precio": 15000,
  "stock": 8,
  "tags": ["portatil", "trabajo"],
  "specs": {"ram_gb": 16, "ssd_gb": 512}
}
```

Por ejemplo, la Laptop incluye el subdocumento `specs`, la Silla incluye `color` y el Escritorio incluye `medidas_cm`. En un modelo relacional estos atributos se traducirían en columnas vacías para la mayoría de los registros; en el modelo documental cada documento almacena únicamente los campos que le corresponden.

## Operaciones implementadas

### CREATE

El método `insert_many` inserta seis documentos en una sola operación. Previamente se ejecuta `delete_many({})` para vaciar la colección, de modo que el script pueda ejecutarse varias veces sin duplicar datos.

### READ

Se realizan dos consultas:

- `find({"categoria": "Computo", "precio": {"$gt": 200}})` obtiene los productos de la categoría Cómputo cuyo precio es mayor a 200, ordenados de mayor a menor precio. El operador `$gt` significa "mayor que".
- `find({"tags": "accesorio"})` busca un valor dentro del arreglo `tags`. El segundo argumento es la proyección, que limita el resultado a los campos `nombre` y `precio`.

### UPDATE

El método `update_one` con el operador `$set` modifica el precio del Mouse de 250 a 300 sin alterar los demás campos del documento.

### DELETE

El método `delete_one` elimina el documento correspondiente a la Silla, con lo que la colección queda con cinco productos.

### Agregación

El método `aggregate` con la etapa `$group` agrupa los documentos por `categoria` y calcula, para cada grupo, la suma de precios y el número de productos. La etapa `$sort` ordena el resultado de mayor a menor. La operación equivale a la siguiente consulta SQL:

```sql
SELECT categoria, SUM(precio) AS total, COUNT(*) AS n
FROM productos
GROUP BY categoria
ORDER BY total DESC
```

## Resultado de la ejecución

```
CREATE - documentos insertados: 6
READ - Computo con precio mayor a 200:
   Laptop - 15000
   Teclado - 900
   Mouse - 250
READ - productos con el tag accesorio:
   {'nombre': 'Mouse', 'precio': 250}
   {'nombre': 'Teclado', 'precio': 900}
UPDATE - documentos modificados: 1 | precio nuevo del Mouse: 300
DELETE - documentos borrados: 1 | quedan: 5
AGREGACION - total por categoria:
   Computo | productos: 3 | suma de precios: 16200
   Oficina | productos: 1 | suma de precios: 3200
   Audio | productos: 1 | suma de precios: 1200
```
