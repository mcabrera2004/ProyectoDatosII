from pymongo import MongoClient
import os

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]

print("Colecciones disponibles:")
print(db.list_collection_names())
