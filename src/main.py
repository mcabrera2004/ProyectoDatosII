from pymongo import MongoClient
import os

def conectar_mongodb():
    try:
        client = MongoClient(os.environ.get("MONGO_URI"))
        print("⚡ Conexión exitosa a MongoDB!")
        return client
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

if __name__ == "__main__":
    client = conectar_mongodb()
    if client:
        try:
            db = client[os.environ.get("DB_NAME")]
            print("Colecciones disponibles:", db.list_collection_names())
        finally:
            client.close()
            print("Conexión cerrada correctamente")
 