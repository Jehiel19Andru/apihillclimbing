import math
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Base de datos simulada de coordenadas
coord = {
    'Jiloyork': (19.916012, -99.580580), 'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844), 'Guadalajara': (20.677754, -103.346253),
    'Monterrey': (25.691611, -100.321838), 'QuintanaRoo': (21.163111, -86.802315),
    'Michoacan': (19.701400, -101.208296), 'Aguascalientes': (21.876410, -102.264386),
    'CDMX': (19.432713, -99.133183), 'QRO': (20.597194, -100.386670)
}

# Calcular distancia entre dos ciudades
def calcular_distancia(ciudad1, ciudad2):
    lat1, lon1 = coord[ciudad1]
    lat2, lon2 = coord[ciudad2]
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

# Hill Climbing para optimización de rutas
def hill_climbing(ciudades):
    random.shuffle(ciudades)
    mejor_ruta = ciudades[:]
    mejor_distancia = sum(calcular_distancia(mejor_ruta[i], mejor_ruta[i+1]) for i in range(len(mejor_ruta)-1))

    for _ in range(1000):  # Iteraciones de mejora
        i, j = random.sample(range(len(ciudades)), 2)
        nueva_ruta = mejor_ruta[:]
        nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
        nueva_distancia = sum(calcular_distancia(nueva_ruta[i], nueva_ruta[i+1]) for i in range(len(nueva_ruta)-1))

        if nueva_distancia < mejor_distancia:
            mejor_ruta, mejor_distancia = nueva_ruta, nueva_distancia

    return mejor_ruta, mejor_distancia

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/random_route', methods=['GET'])
def random_route():
    ciudades = list(coord.keys())
    ruta_optima, distancia = hill_climbing(ciudades)
    return jsonify({"ruta": ruta_optima, "distancia": distancia})

if __name__ == '__main__':
    app.run(debug=True)
