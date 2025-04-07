# src/api.py
from flask import Flask, render_template
from pymongo import MongoClient
import os


app = Flask(__name__, template_folder="../templates")

# Configuración de MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coleccion = db["testeo"]

@app.route('/', methods=['GET'])
def home():
    """Ruta de inicio"""
    return render_template('index.html')

'''@app.route('/destinos', methods=['GET'])
def obtener_destinos():
    """Obtiene todos los destinos turísticos"""
    try:
        destinos = list(coleccion.find({}, {'_id': 0}))
        return jsonify({"data": destinos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/destinos/<clima>', methods=['GET'])
def filtrar_por_clima(clima):
    """Filtra destinos por tipo de clima"""
    try:
        resultados = list(coleccion.find(
            {"clima": clima},
            {'_id': 0, 'nombre': 1, 'pais': 1, 'clima': 1}
        ))
        return jsonify({"count": len(resultados), "data": resultados}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/estadisticas', methods=['GET'])
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
        return jsonify({"error": str(e)}), 500

#@app.route('/recomendar/<tipo>', methods=['GET'])
#def recomendar(tipo):
    """Recomienda destinos por tipo de actividad"""
    try:
        recomendaciones = list(coleccion.find(
            {"actividades": tipo.lower()},
            {'_id': 0, 'nombre': 1, 'actividades': 1, 'puntuacion': 1}
        ).sort("puntuacion", -1).limit(5))
        
        return jsonify({
            "tipo_actividad": tipo,
            "resultados": recomendaciones
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)