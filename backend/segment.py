from flask import Flask, request, jsonify, send_file, url_for
from ultralytics import YOLO
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Load a model
model = YOLO('best.pt')  # pretrained YOLOv8n model

@app.route('/segment', methods=['POST'])
def segment_image():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    # Convertir el blob a imagen
    image_file = Image.open(io.BytesIO(image_file.read()))
    print("Archivo recibido", image_file)
    # Run inference on the uploaded image
    results = model(image_file)

    # Assuming only one result is returned
    result = results[0]

    # Save the segmented image to a temporary file
    segmented_image_path = 'segmented.jpg'
    result.save(filename=segmented_image_path)

    # Create response with CORS headers
    response = {
        'segmentacion': url_for('static', filename='segmented.jpg')
    }
    print("Respuesta", response)
    return jsonify(response), 200

@app.route('/segmented-image', methods=['GET'])
def get_segmented_image():
    # Return the segmented image as a file
    return send_file('segmented.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
