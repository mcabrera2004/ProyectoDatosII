from pymongo import MongoClient
from faker import Faker
import json
import os

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
collection_name = "testeo"

fake = Faker('es_ES')
destinos = []

for i in range(15):
    destino = {
        "nombre": fake.city(),
        "pais": fake.country(),
        "clima": fake.random_element(["Tropical", "Templado", "Árido", "Mediterráneo", "Continental", "Polar", "Desértico", "Seco"]),
        "actividades": fake.words(nb=3, unique=True),
        "costo_promedio": fake.random_int(500, 5000),
        "puntuacion": fake.random_int(1, 5)
    }
    destinos.append(destino)

with open("data/destinos.json", "w", encoding="utf-8") as f:
    json.dump(destinos, f, ensure_ascii=False, indent=4)

try:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    result = collection.insert_many(destinos)
    print(f"Se insertaron {len(result.inserted_ids)} documentos en esta colección")
except Exception as e:
    print(f"Error al insertar documentos: {e}")
finally:
    client.close()
    print("Conexión cerrada")

