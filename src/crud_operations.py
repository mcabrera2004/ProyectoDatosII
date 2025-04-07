from main import conectar_mongodb

db = conectar_mongodb()
coleccion = db["testeo"]

# CREATE
def insertar_destino(destino):
    return coleccion.insert_one(destino).inserted_id

def insertar_varios_destinos(destinos):
    resultado = coleccion.insert_many(destinos)
    return resultado.inserted_ids

# READ
def obtener_destinos(filtro={}):
    return list(coleccion.find(filtro, {"_id": 0}))

# UPDATE
def actualizar_destino(filtro, nuevos_valores):
    return coleccion.update_many(filtro, {"$set": nuevos_valores})

# DELETE
def eliminar_destino(filtro):
    return coleccion.delete_many(filtro)