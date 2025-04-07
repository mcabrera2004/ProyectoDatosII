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

    # Vaciar la colección
    result = collection.delete_many({})
    
    # Mostrar resultado
    print(f"Se eliminaron {result.deleted_count} documentos de la colección '{collection_name}'")
    
    # Verificar que la colección está vacía
    count_after = collection.count_documents({})
    print(f"Documentos en la colección '{collection_name}' después de vaciar: {count_after}")

except Exception as e:
    print(f"Error al vaciar la colección: {e}")
finally:
    client.close()
    print("Conexión cerrada")