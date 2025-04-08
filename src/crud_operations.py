from main import obtener_base_datos

db = obtener_base_datos()
coleccion = db["testeo"]

# CREATE
def insertar_destino(destino):
    return coleccion.insert_one(destino).inserted_id

# READ
def obtener_destinos(filtro={}):
    return list(coleccion.find(filtro))

# UPDATE
def actualizar_destino(filtro, nuevos_valores):
    return coleccion.update_many(filtro, {"$set": nuevos_valores})

# DELETE
def eliminar_destino(filtro):
    return coleccion.delete_many(filtro)