from pymongo import MongoClient
from faker import Faker
from crud_operations import registrar_evento
from bson import ObjectId
import os

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
collection_name = "testeo"

fake = Faker('es_ES')  # Cambia el locale a español para generar datos en español

# Generar datos falsos
def generar_datos_falsos():
    return {
        "nombre": fake.city(),
        "pais": fake.country(),
        "clima": fake.random_element(elements=["Desértico", "Tropical", "Templado", "Frío"]),
        "actividades": fake.random_elements(elements=["laborum", "exercitationem", "voluptas", "aventura", "relax"], length=3, unique=True),
        "costo_promedio": fake.random_int(min=500, max=5000),
        "puntuacion": fake.random_int(min=1, max=5)
    }
def consultar_documentos(collection):
    print(f"Consultando todos los documentos en la colección '{collection_name}':")
    documentos = collection.find()
    for doc in documentos:
        print(doc)

try:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    print(f"Insertando datos en la colección '{collection_name}'...")
    datos_falsos = [generar_datos_falsos() for i in range(10)] 
    collection.insert_many(datos_falsos)
    print("Datos insertados correctamente.")

    print(f"Documentos en la colección '{collection_name}':")
    consultar_documentos(collection)

    for i, documento in enumerate(datos_falsos):
        print(f"Registrando documento {i+1}/10")
        registrar_evento("insert", {"datos": documento})
    print("Todos los documentos han sido registrados.")

except Exception as e:
    print(f"Error al realizar operaciones en la base de datos: {e}")
finally:
    client.close()
    print("Conexión cerrada")