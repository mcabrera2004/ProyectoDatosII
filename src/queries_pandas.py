import pandas as pd
import os
from BBDD import obtener_base_datos

db = obtener_base_datos()
coleccion = db["testeo"]

directorio_src = os.path.dirname(__file__)
carpeta_reportes = os.path.join(directorio_src, "reportes")

# 1. Listar destinos con costo_promedio mayor a 1500
consulta1 = list(coleccion.find({"costo_promedio": {"$gt": 1500}}))
df1 = pd.DataFrame(consulta1)
ruta_csv1 = os.path.join(carpeta_reportes, "destinos_costo_alto.csv")
df1.to_csv(ruta_csv1, index=False)
print("Exportado: destinos_costo_alto.csv")

# 2. Agrupar destinos por país y calcular el costo promedio de cada uno
pipeline_pais = [
    {"$group": {"_id": "$pais", "costo_promedio": {"$avg": "$costo_promedio"}}},
    {"$sort": {"costo_promedio": -1}}
]
consulta2 = list(coleccion.aggregate(pipeline_pais))
df2 = pd.DataFrame(consulta2)
ruta_csv2 = os.path.join(carpeta_reportes, "destinos_por_pais_costo_promedio.csv")
df2.to_csv(ruta_csv2, index=False)
print("Exportado: destinos_por_pais_costo_promedio.csv")

# 3. Agrupar destinos por clima y contar cuántos hay en cada grupo
pipeline = [
    {"$group": {"_id": "$clima", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
consulta3 = list(coleccion.aggregate(pipeline))
df3 = pd.DataFrame(consulta3)
ruta_csv3 = os.path.join(carpeta_reportes, "destinos_por_clima.csv")
df3.to_csv(ruta_csv3, index=False)
print("Exportado:", ruta_csv3)

# 4. Listar destinos con puntuacion mayor a 3
consulta4 = list(coleccion.find({"puntuacion": {"$gt": 3}}))
df4 = pd.DataFrame(consulta4)
ruta_csv4 = os.path.join(carpeta_reportes, "destinos_puntuacion_alta.csv")
df4.to_csv(ruta_csv4, index=False)
print("Exportado:", ruta_csv4)

# 5. Listar destinos que tengan "senderismo" en actividades
consulta5 = list(coleccion.find({"actividades": "senderismo"}))
df5 = pd.DataFrame(consulta5)
ruta_csv5 = os.path.join(carpeta_reportes, "destinos_senderismo.csv")
df5.to_csv(ruta_csv5, index=False)
print("Exportado:", ruta_csv5)