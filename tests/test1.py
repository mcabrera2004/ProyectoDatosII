from pymongo import MongoClient
import os

# Configuración de conexión
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
collection_name = "testeo"

try:
    # Conexión a MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Consultar todos los documentos de la colección
    print(f"Documentos en la colección '{collection_name}':")
    for doc in collection.find():
        print(doc)

except Exception as e:
    print(f"Error al consultar la base de datos: {e}")
finally:
    client.close()
    print("Conexión cerrada")