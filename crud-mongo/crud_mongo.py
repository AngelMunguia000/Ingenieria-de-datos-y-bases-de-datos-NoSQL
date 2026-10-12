import mongomock

# Opción B de la guía: mongomock simula MongoDB en memoria, no necesita servidor.
# Para usar un MongoDB real, cambia las dos líneas de conexión por:
#   from pymongo import MongoClient
#   client = MongoClient("mongodb://localhost:27017/")  # o la cadena de Atlas
client = mongomock.MongoClient()

db = client["tienda"]
productos = db["productos"]
productos.delete_many({})  # limpiar antes de empezar

# ===== CREATE: insertar documentos (flexibles, tipo JSON) =====
productos.insert_many([
    {"nombre": "Laptop", "categoria": "Computo", "precio": 15000, "stock": 8,
     "tags": ["portatil", "trabajo"], "specs": {"ram_gb": 16, "ssd_gb": 512}},
    {"nombre": "Mouse", "categoria": "Computo", "precio": 250, "stock": 40,
     "tags": ["accesorio"]},
    {"nombre": "Teclado", "categoria": "Computo", "precio": 900, "stock": 25,
     "tags": ["accesorio", "mecanico"]},
    {"nombre": "Silla", "categoria": "Oficina", "precio": 1800, "stock": 5,
     "tags": ["ergonomica"], "color": "negro"},
    {"nombre": "Escritorio", "categoria": "Oficina", "precio": 3200, "stock": 3,
     "medidas_cm": {"largo": 120, "ancho": 60}},
    {"nombre": "Audifonos", "categoria": "Audio", "precio": 1200, "stock": 15,
     "tags": ["bluetooth"]},
])
print("CREATE - documentos insertados:", productos.count_documents({}))

# ===== READ: consultar con filtros (categoría Computo y precio > 200) =====
print("READ - Computo con precio mayor a 200:")
filtro = {"categoria": "Computo", "precio": {"$gt": 200}}
for d in productos.find(filtro).sort("precio", -1):
    print("  ", d["nombre"], "-", d["precio"])

print("READ - productos con el tag accesorio:")
for d in productos.find({"tags": "accesorio"}, {"_id": 0, "nombre": 1, "precio": 1}):
    print("  ", d)

# ===== UPDATE: actualizar el precio del Mouse =====
res = productos.update_one({"nombre": "Mouse"}, {"$set": {"precio": 300}})
print("UPDATE - documentos modificados:", res.modified_count,
      "| precio nuevo del Mouse:", productos.find_one({"nombre": "Mouse"})["precio"])

# ===== DELETE: borrar la Silla =====
res = productos.delete_one({"nombre": "Silla"})
print("DELETE - documentos borrados:", res.deleted_count,
      "| quedan:", productos.count_documents({}))

# ===== Agregación: total por categoría (equivalente a GROUP BY) =====
pipeline = [
    {"$group": {"_id": "$categoria",
                "total": {"$sum": "$precio"},
                "n": {"$sum": 1}}},
    {"$sort": {"total": -1}},
]
print("AGREGACION - total por categoria:")
for g in productos.aggregate(pipeline):
    print("  ", g["_id"], "| productos:", g["n"], "| suma de precios:", g["total"])
