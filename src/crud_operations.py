from main import obtener_base_datos

db = obtener_base_datos()
coleccion = db["testeo"]

# CREATE
def insertar_destino(destino):
    return coleccion.insert_one(destino).inserted_id

def insertar_varios_destinos(destinos):
    resultado = coleccion.insert_many(destinos)
    return resultado.inserted_ids

# READ
def obtener_destinos(params={}):
    filtro = {}
    # Campos de texto
    for campo in ['nombre', 'pais', 'clima', 'actividades']:
        if valor := params.get(campo):
            filtro[campo] = valor

# Campos numéricos
    for campo in ['costo_promedio', 'puntuacion']:
        if valor := params.get(campo):
            try:
                filtro[campo] = int(valor)
            except ValueError:
                pass
        return list(coleccion.find(filtro, {"_id": 0}))

# UPDATE
def actualizar_destino(filtro, nuevos_valores):
    return coleccion.update_many(filtro, {"$set": nuevos_valores})

# DELETE
def eliminar_destino(filtro):
    return coleccion.delete_many(filtro)

'''def agregar_destinos():
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
'''

