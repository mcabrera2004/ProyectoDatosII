from pymongo import MongoClient
import os

def conectar_mongodb():
    try:
        client = MongoClient("mongodb+srv://equipo_viajes:equipopassword@ingdatos.hzoisln.mongodb.net/viajes_recomendacion?retryWrites=true&w=majority&authSource=admin")
        print("⚡ Conexión exitosa a MongoDB!")
        return client
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None


def obtener_base_datos():
    try:
        client = conectar_mongodb()
        return client[os.environ.get("DB_NAME")]
    except Exception as e:
        print(f"Error al obtener la base de datos: {e}")
        return None
 