# Ingeniería de datos y bases de datos NoSQL

Prácticas de la asignatura Optativa III: Ciencia de Datos, UNE Plantel Centro.

**Autor:** Angel David Munguía Zúñiga

## Contenido del repositorio

| Práctica | Ubicación | Descripción |
|---|---|---|
| Pipeline ETL de ventas | Raíz del repositorio | Pipeline que carga un archivo CSV en una base de datos SQLite con esquema estrella |
| Operaciones CRUD en MongoDB | [`crud-mongo/`](crud-mongo/) | Modelado de una colección documental, operaciones CRUD y agregación |

---

# Pipeline ETL de ventas

Práctica de la Semana 6. El script `etl.py` implementa un pipeline ETL que extrae las ventas de un archivo CSV, genera una columna calculada, modela los datos en un esquema estrella y los carga en una base de datos SQLite.

## Ejecución

```
pip install pandas
python etl.py
```

El archivo `almacen.db` no se incluye en el repositorio porque el script lo genera en cada ejecución.

## Fases del pipeline

### Extracción (Extract)

Se lee el archivo `ventas.csv` con pandas. El resultado es un conjunto de 14 registros con las columnas `producto`, `categoria`, `precio` y `cantidad`.

### Transformación (Transform)

Se calcula la columna `total` como el producto de `precio` por `cantidad`. Posteriormente, las categorías distintas se separan en una tabla independiente, a cada una se le asigna un identificador `cat_id` y, en la tabla de ventas, el nombre de la categoría se sustituye por dicho identificador.

### Carga (Load)

Las dos tablas se almacenan en `almacen.db` mediante el método `to_sql`. Se utiliza la opción `replace` para evitar que los datos se dupliquen cuando el script se ejecuta más de una vez.

## Esquema estrella

- **Tabla de hechos `fact_ventas`:** cada fila representa una venta, con sus métricas `precio`, `cantidad` y `total`, y la clave `cat_id`.
- **Dimensión `dim_categoria`:** contiene el identificador `cat_id` y el nombre de la categoría.

Con este diseño, el nombre de cada categoría se almacena una sola vez y el cálculo de ingresos por categoría requiere únicamente una operación JOIN entre ambas tablas.

## Consulta de verificación

```sql
SELECT d.categoria, COUNT(*) AS num_ventas, SUM(f.total) AS ingresos
FROM fact_ventas f
JOIN dim_categoria d ON f.cat_id = d.cat_id
GROUP BY d.categoria
ORDER BY ingresos DESC
```

## Resultado de la ejecución

La salida del script muestra que la categoría Cómputo es la que genera mayores ingresos.

```
Extraídas 14 filas
Cargadas 5 categorías y 14 ventas en almacen.db
    categoria  num_ventas  ingresos
0     Cómputo           4     46600
1     Oficina           3     15850
2       Audio           3     12900
3  Accesorios           2      6300
4   Papelería           2      2850
```
