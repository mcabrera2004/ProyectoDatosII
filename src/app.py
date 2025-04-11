from flask import Flask, request, render_template, url_for, redirect
from pymongo import MongoClient
import os
from bson import ObjectId
from crud_operations import insertar_destino, obtener_destinos, actualizar_destino, eliminar_destino


app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configuración de MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coleccion = db["testeo"]

# ---------------------------------------------------------------- MAIN

#Ruta de Inicio
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# ---------------------------------------------------------------- CREATE

@app.route('/crear_destino', methods=['GET', 'POST'])
def crear_destino():
    if request.method == 'POST':
        destino = {
            "nombre": request.form.get('nombre'),
            "pais": request.form.get('pais'),
            "clima": request.form.get('clima'),
            "actividades": [act.strip() for act in request.form.get('actividades').split(',')],
            "costo_promedio": int(request.form.get('costo_promedio')),
            "puntuacion": int(request.form.get('puntuacion'))
        }
        insertar_destino(destino)
        return redirect(url_for('filtro_destinos'))
    
    # Si es GET, mostrar el formulario para crear destino
    return render_template('crear_destino.html') 
   
# ---------------------------------------------------------------- READ
    
@app.route('/destinos', methods=['GET'])
def filtro_destinos():
    try:
        params = request.args.to_dict()
        destinos = obtener_destinos(params)
        return render_template('destinos.html', destinos=destinos)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

# ---------------------------------------------------------------- UPDATE

@app.route('/editar_destino/<id>', methods=['GET', 'POST'])
def editar_destino(id):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nuevos_valores = {
            "nombre": request.form.get('nombre'),
            "pais": request.form.get('pais'),
            "clima": request.form.get('clima'),
            "actividades": request.form.get('actividades').split(','),
            "costo_promedio": int(request.form.get('costo_promedio')),
            "puntuacion": int(request.form.get('puntuacion'))
        }
        # Actualizar el destino en la base de datos
        actualizar_destino({"_id": ObjectId(id)}, nuevos_valores)
        return redirect(url_for('filtro_destinos'))

    # Obtener el destino actual desde la base de datos
    destino = coleccion.find_one({"_id": ObjectId(id)})
    if not destino:
        return render_template('error.html', mensaje="Destino no encontrado"), 404

    return render_template('editar_destino.html', destino=destino)

# ---------------------------------------------------------------- DELETE

@app.route('/eliminar_destino_ruta/<id>', methods=['POST'])
def eliminar_destino_ruta(id):
    try:
        eliminar_destino({"_id": ObjectId(id)})
        return redirect(url_for('filtro_destinos'))
    except Exception as e:
        return render_template('error.html', mensaje=str(e))

# ----------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)