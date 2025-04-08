from main import obtener_base_datos

db = obtener_base_datos()
coleccion = db["testeo"]

documentos = coleccion.find()
for documento in documentos:
    print(documento)




