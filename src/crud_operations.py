from BBDD import obtener_base_datos
from faker import Faker
import json
import os
import datetime
fake = Faker('es_ES')
db = obtener_base_datos()
coleccion = db["testeo"]
collection_name = coleccion.name

#------------------------------------------------------------------------------------

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'destinos.json')

def registrar_evento(evento, documento):
    try:
        try:
            print("Iniciando registrar_evento:", evento)
            print("Documento recibido:", documento)

            documento_serializable = json.loads(json.dumps(documento, default=str))
            print("Documento serializado correctamente")
        except Exception as json_error:
            print("Error al serializar el documento:", str(json_error))

        try:   
            with open(DATA_FILE, 'r') as f:
                datos = json.load(f)
            print("Datos cargados correctamente")
        except json.JSONDecodeError:
            print("Archivo JSON vacío o no válido, creando nuevo archivo")
            datos = []
                
        datos.append({
            "evento": evento,
            "documento": documento_serializable,
            "timestamp": str(datetime.datetime.now())
        })
        print("Escribiendo datos en archivo JSON")
        with open(DATA_FILE, 'w') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        print("Datos guardados correctamente en", DATA_FILE)

    except Exception as e:
        print(f"Error al registrar evento en JSON: {e}")


#------------------------------------------------------------------------------------

# CREATE
def insertar_destino(destino):
    result = coleccion.insert_one(destino).inserted_id
    registrar_evento("insert", {"datos": destino})
    return result

def insertar_varios_destinos(cantidad):
    documentos = []
    for i in range(cantidad):
        destino = {
            "nombre": fake.city(),
            "pais": fake.country(),
            "clima": fake.random_element(
                elements=[
                    "Desértico", "Tropical", "Templado", "Frío",
                    "Lluvioso", "Nublado", "Ventoso", "Soleado", "Húmedo", "Seco"
                ]
            ),
            "actividades": fake.random_elements(
                elements=["senderismo", "natación", "ciclismo", "ski", "fotografía", "gastronomía", "festival"],
                length=3, 
                unique=True
            ),
            "costo_promedio": fake.random_int(min=100, max=2000),
            "puntuacion": fake.random_int(min=1, max=5)
        }
        documentos.append(destino)

    # Se guardan los documentos en un JSON temporal para evitar duplicados
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'destinos_temp.json')
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(documentos, f, indent=4, ensure_ascii=False)

    # Cargar los datos desde el archivo JSON temporal
    with open(json_file_path, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    # Insertar los datos en la colección y registrar cada inserción en destinos.json
    resultado = coleccion.insert_many(datos)
    for destino in datos:
        registrar_evento("insert_many", {"datos": destino})
    
    # Eliminar el archivo temporal después de la carga
    os.remove(json_file_path)

    return resultado.inserted_ids

#------------------------------------------------------------------------------------

# READ
def obtener_destinos(params={}):
    filtro = {}
    # Campos de texto simples
    for campo in ['nombre', 'pais', 'clima']:
        if valor := params.get(campo):
            filtro[campo] = valor
    
    # Campo de actividades (tratado como array)
    if actividades := params.get('actividades'):
        lista_actividades = [act.strip() for act in actividades.split(',')]
        if len(lista_actividades) == 1:
            filtro['actividades'] = lista_actividades[0]
        else:
            # Busca destinos que contengan CUALQUIERA de las actividades
            filtro['actividades'] = {'$in': lista_actividades}

    # Campos numéricos
    for campo in ['costo_promedio', 'puntuacion']:
        if valor := params.get(campo):
            try:
                filtro[campo] = int(valor)
            except ValueError:
                pass
    
    return list(coleccion.find(filtro))

#------------------------------------------------------------------------------------

# UPDATE
def actualizar_destino(filtro, nuevos_valores):
    result = coleccion.update_many(filtro, {"$set": nuevos_valores})
    registrar_evento("update", {"filtro": filtro, "nuevos_valores": nuevos_valores})
    return result

#------------------------------------------------------------------------------------

# DELETE
def eliminar_destino(filtro):
    result = coleccion.delete_many(filtro)
    registrar_evento("delete", {"filtro": filtro})
    return result

def eliminar_todos_los_destinos():
    documentos_a_eliminar = list(coleccion.find({}))
    result = coleccion.delete_many({})
    print(f"Se eliminaron {result.deleted_count} documentos de la colección '{collection_name}'")
    for documento in documentos_a_eliminar:
        registrar_evento("delete_all", {"datos": documento})
    count_after = coleccion.count_documents({})
    print(f"Documentos en la colección '{collection_name}' después de vaciar: {count_after}")
    return result

#------------------------------------------------------------------------------------

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

