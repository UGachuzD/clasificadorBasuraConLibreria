from flask import Flask, request, jsonify, send_file, url_for
from ultralytics import YOLO
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

model = YOLO('best.pt') 

@app.route('/segment', methods=['POST'])
def segmentarImagen():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    archivoImagen = request.files['image']
    # Convertir el blob a imagen
    archivoImagen = Image.open(io.BytesIO(archivoImagen.read()))
    print("Archivo recibido", archivoImagen)
    results = model(archivoImagen)
    result = results[0]
    rutaImagenSegmentada = 'segmented.jpg'
    result.save(filename=rutaImagenSegmentada)

    response = {
        'segmentacion': url_for('static', filename='segmented.jpg')
    }
    print("Respuesta", response)
    return jsonify(response), 200

@app.route('/segmented-image', methods=['GET'])
def getImagenSegmentada():
    return send_file('segmented.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
