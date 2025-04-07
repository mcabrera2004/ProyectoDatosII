from flask import Flask, request, jsonify
from crud_operation import (
    insertar_destino,
    insertar_varios_destinos,
    obtener_destinos,
    actualizar_destino,
    eliminar_destino
)
from faker import Faker
from pymongo import MongoClient
import os

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")
collection_name = "destinos"

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]
import random

app = Flask(__name__)
fake = Faker()

# Función para generar un destino aleatorio
def generar_destino_fake():
    return {
        "nombre": fake.city(),
        "pais": fake.country(),
        "clima": random.choice(["Tropical", "Seco", "Nevado", "Desértico", "Templado"]),
        "actividades": random.sample(
            ["surf", "misterios", "bicicleta", "museos", "expediciones", "kayak", "escalada"],
            3
        ),
        "costo_promedio": random.randint(500, 5000),
        "puntuacion": random.randint(1, 5)
    }

# Función para insertar datos
@app.route("/dstinos")
def agregar_destinos():
    #Agregar datos manualmente
    destinos_manuales = [
        {
            "nombre": "IsladelSol",
            "pais": "Nubaria",
            "clima": "Tropical",
            "actividades": ["surf", "kayak", "expediciones"],
            "costo_promedio": 2500,
            "puntuacion": 4
        },
        {
            "nombre": "Ventisquero",
            "pais": "Glacierland",
            "clima": "Nevado",
            "actividades": ["escalada", "misterios", "museos"],
            "costo_promedio": 3100,
            "puntuacion": 5
        },
        {
            "nombre": "Oasiria",
            "pais": "Desertia",
            "clima": "Desértico",
            "actividades": ["bicicleta", "expediciones", "museos"],
            "costo_promedio": 1800,
            "puntuacion": 3
        }
    ]

    #Agregar datos autogenerados
    destinos_fake = [generar_destino_fake() for _ in range(3)]

    destinos = destinos_manuales + destinos_fake
    #para que cada vez que se dirige a /destinos se pisen los datos y no  haya duplicados
    for destino in destinos:
        collection.update_one(
            {"nombre": destino["nombre"]},  # Si existe este nombre, se actualiza
            {"$set": destino},              # Si no existe, se inserta
            upsert=True                     # Esto permite insertar si no está
        )

    client.close()
    return jsonify({"mensaje": "Se insertaron destinos manuales y aleatorios", "destinos": destinos})
    


# Obtiene todos los destinos
@app.route("/destinos", methods=["GET"])
def listar_destinos():
    filtro = request.args.to_dict()
    destinos = obtener_destinos(filtro)
    return jsonify(destinos)

#Filtros
@app.route("/filtros", methods=["GET"])
def listar_destinos():
    args = request.args.to_dict()
    filtro = {}

    # Filtro por país
    if "pais" in args:
        filtro["pais"] = args["pais"]

    # Filtro por clima
    if "clima" in args:
        filtro["clima"] = args["clima"]

    # Filtro por actividad (debe estar en la lista de actividades)
    if "actividad" in args:
        filtro["actividades"] = args["actividad"]

    # Filtro por puntuación mínima
    if "min_puntuacion" in args:
        filtro["puntuacion"] = {"$gte": int(args["min_puntuacion"])}

    # Filtro por costo mínimo y/o máximo
    if "min_costo" in args or "max_costo" in args:
        filtro["costo_promedio"] = {}
        if "min_costo" in args:
            filtro["costo_promedio"]["$gte"] = int(args["min_costo"])
        if "max_costo" in args:
            filtro["costo_promedio"]["$lte"] = int(args["max_costo"])

    destinos = obtener_destinos(filtro)
    return jsonify(destinos)




@app.route("/actualizar")
def actualizar_destinos():
    # 1. Cambiar país
    actualizar_destino({"pais": "Zarlandia"}, {"pais": "Argentina"})

    # 2. Aumentar puntuación de destinos con puntuación 1 a 3
    actualizar_destino({"puntuacion": 1}, {"puntuacion": 3})

    # 3. Cambiar clima de "Desértico" a "Tropical"
    actualizar_destino({"clima": "Desértico"}, {"clima": "Tropical"})

    # 4. Cambiar país a "Chile" donde el nombre sea "Bravonia"
    actualizar_destino({"nombre": "Bravonia"}, {"pais": "Chile"})

    # 5. Aumentar el costo de destinos con puntuación mayor o igual a 4
    actualizar_destino({"puntuacion": {"$gte": 4}}, {"costo_promedio": 9999})

    # 6. Agregar actividad a destinos con clima "Seco"
    actualizar_destino({"clima": "Seco"}, {"actividades": ["misterios", "expediciones", "kayak"]})

    # 7. Cambiar todos los destinos de "Mykon" a "Uruguay"
    actualizar_destino({"pais": "Mykon"}, {"pais": "Uruguay"})

    return jsonify({"mensaje": "Actualizaciones aplicadas correctamente"})




if __name__ == '__main__':
    
    app.run(debug=True)

