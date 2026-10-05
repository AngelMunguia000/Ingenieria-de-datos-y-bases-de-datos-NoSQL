# ETL de ventas

practica de la semana 6 de ciencia de datos. hice un pipeline que lee un csv de ventas, le agrega una columna nueva y lo guarda en una base sqlite con esquema estrella

## como correrlo

```
pip install pandas
python etl.py
```

el archivo almacen.db no lo subi por que se crea solo al correr el script

## extract

leo ventas.csv con pandas y me quedan 14 filas con producto, categoria, precio y cantidad

## transform

saque la columna total multiplicando precio por cantidad. depsues separe las categorias que no se repiten en otra tabla y a cada una le puse un cat_id, y en las ventas cambie el nombre de la categoira por ese numero

## load

las dos tablas se guardan en almacen.db con to_sql. le puse replace para que no se dupliquen los datos si lo corro otra ves

## esquema estrella

fact_ventas es la tabla de hechos, cada fila es una venta con su precio, cantidad, total y el cat_id. dim_categoria es la dimension y solo tiene el cat_id con el nombre de la categoria. asi el nombre se guarda una sola ves y para sacar los ingresos por categoria nada mas ahi que hacer un join

## consulta final

```sql
SELECT d.categoria, COUNT(*) AS num_ventas, SUM(f.total) AS ingresos
FROM fact_ventas f
JOIN dim_categoria d ON f.cat_id = d.cat_id
GROUP BY d.categoria
ORDER BY ingresos DESC
```

esto sale al correr el script, computo es la que mas ingresos tiene

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
