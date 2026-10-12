# CRUD en MongoDB desde Python

Práctica de Optativa III: Ciencia de Datos, UNE Plantel Centro.
Script en Python que modela una colección documental de productos y realiza las cuatro operaciones CRUD más una agregación por categoría.

Autor: Angel David Munguía Zúñiga

## Archivos

| Archivo | Descripción |
|---|---|
| `crud_mongo.py` | Script con la conexión, las cuatro operaciones CRUD y la agregación |
| `requirements.txt` | Librerías que se instalan con pip |

## Cómo ejecutarlo

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python crud_mongo.py
```

## Conexión a MongoDB

Se usa la Opción B de la guía: `mongomock`, que simula MongoDB en memoria con la misma sintaxis de `pymongo` y no necesita servidor.

```python
import mongomock
client = mongomock.MongoClient()
```

Para correrlo contra un MongoDB real solo cambian esas dos líneas, el resto del script queda igual:

```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")  # o la cadena de MongoDB Atlas
```

Después se elige la base `tienda` y la colección `productos`. MongoDB las crea solas al insertar el primer documento, no hay que definir tablas ni columnas antes.

## Modelo de la colección

Cada producto es un documento tipo JSON. Todos tienen `nombre`, `categoria`, `precio` y `stock`, pero cada uno puede llevar campos propios:

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

La Laptop tiene `specs`, la Silla tiene `color` y el Escritorio tiene `medidas_cm`. En una tabla relacional eso serían columnas vacías en casi todas las filas, aquí cada documento guarda solo lo que le corresponde.

## Operaciones

### CREATE
`insert_many` inserta seis productos de una sola vez. Antes se ejecuta `delete_many({})` para que el script se pueda correr varias veces sin duplicar datos.

### READ
- `find({"categoria": "Computo", "precio": {"$gt": 200}})` trae los productos de Cómputo con precio mayor a 200, ordenados del más caro al más barato. `$gt` es el operador "mayor que".
- `find({"tags": "accesorio"})` busca dentro del arreglo `tags`. El segundo parámetro es la proyección, que deja solo `nombre` y `precio`.

### UPDATE
`update_one` con `$set` cambia el precio del Mouse de 250 a 300 sin tocar los demás campos del documento.

### DELETE
`delete_one` borra el documento de la Silla, quedan cinco productos.

### Agregación
`aggregate` con `$group` agrupa por `categoria` y calcula la suma de precios y el número de productos de cada grupo. Es el equivalente a esta consulta SQL:

```sql
SELECT categoria, SUM(precio) AS total, COUNT(*) AS n
FROM productos
GROUP BY categoria
ORDER BY total DESC
```

## Salida del programa

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
