from flask import Flask, jsonify, request, render_template
import tracker  

app = Flask(__name__)

@app.route('/')
def home():
    # Renderiza la página inicial con el formulario de seguimiento
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    # Extrae el número de seguimiento de la solicitud JSON
    tracking_number = request.json.get('trackingNumber')
    if not tracking_number:
        # Retorna un error si no se proporciona el número de seguimiento
        return jsonify({"error": "Tracking number is required"}), 400
    
    try:
        # Llama a la función para rastrear el paquete y obtener detalles
        details = tracker.track_package(tracking_number)
        if details:
            # Devuelve el éxito y los detalles obtenidos si todo fue bien
            return jsonify({"status": "éxito", "detalle": details})
        else:
            # Maneja el caso donde no se encontraron detalles
            return jsonify({"status": "error", "mensaje": "No se han encontrado detalles para este número de seguimiento"}), 404
    except Exception as e:
        # Maneja cualquier otra excepción que pueda ocurrir
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    # Configura el servidor para correr en modo debug durante el desarrollo
    # Recuerda cambiarlo a False cuando estés en producción
    app.run(debug=True)
