import pandas as pd
import sqlite3

# ===== EXTRACT: leer los datos de la fuente =====
df = pd.read_csv("ventas.csv")
print("Extraídas", len(df), "filas")

# ===== TRANSFORM: limpiar y crear una feature nueva =====
df["total"] = df["precio"] * df["cantidad"]   # ingreso por venta

# Modelado dimensional: esquema estrella
dim_categoria = pd.DataFrame({"categoria": df["categoria"].unique()})
dim_categoria["cat_id"] = range(1, len(dim_categoria) + 1)

fact = df.merge(dim_categoria, on="categoria")
fact_ventas = fact[["producto", "cat_id", "precio", "cantidad", "total"]]

# ===== LOAD: cargar a SQLite =====
conn = sqlite3.connect("almacen.db")
dim_categoria.to_sql("dim_categoria", conn, if_exists="replace", index=False)
fact_ventas.to_sql("fact_ventas", conn, if_exists="replace", index=False)
print("Cargadas", len(dim_categoria), "categorías y", len(fact_ventas), "ventas en almacen.db")

# ===== Consulta analítica (esquema estrella en acción) =====
query = """
SELECT d.categoria, COUNT(*) AS num_ventas, SUM(f.total) AS ingresos
FROM fact_ventas f
JOIN dim_categoria d ON f.cat_id = d.cat_id
GROUP BY d.categoria
ORDER BY ingresos DESC
"""
print(pd.read_sql(query, conn))
conn.close()
