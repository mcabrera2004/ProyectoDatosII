# src/api.py
from flask import Flask, render_template
from pymongo import MongoClient
import os
from crud_operations import insertar_destino, obtener_destinos, actualizar_destino, eliminar_destino


app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Configuración de MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coleccion = db["testeo"]

#Ruta de Inicio
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#Obtener todos los destinos turísticos
@app.route('/destinos', methods=['GET'])
def filtro_destinos():
    try:
        destinos = obtener_destinos()
        return render_template('destinos.html', destinos=destinos)
    except Exception as e:
        return render_template('error.html', mensaje=str(e))


'''@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    """Obtiene estadísticas de precios por clima"""
    try:
        pipeline = [
            {"$group": {
                "_id": "$clima",
                "total_destinos": {"$sum": 1},
                "precio_promedio": {"$avg": "$costo_promedio"},
                "precio_maximo": {"$max": "$costo_promedio"},
                "precio_minimo": {"$min": "$costo_promedio"}
            }}
        ]
        stats = list(coleccion.aggregate(pipeline))
        return jsonify({"data": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)