from flask import Flask, render_template, request, jsonify
from pricecomparison import object_recognition, get_google_shopping_prices
from flask_cors import CORS
from PIL import Image
from io import BytesIO


app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_objects', methods=['POST'])
def detect_objects_route():
    image_file = request.files['file']
    if image_file:
        # Convert FileStorage object to PIL Image object
        image = Image.open(BytesIO(image_file.read()))
        detected_objects = object_recognition(image)
        # return jsonify(detected_objects)
        return jsonify(detected_objects)
    else:
        return jsonify({'error': 'No image uploaded'})

@app.route('/scrape_prices', methods=['POST'])
def scrape_prices_route():
    object_name = request.form['object']
    if object_name:
        prices_info = get_google_shopping_prices(object_name)
        return jsonify(prices_info)
    else:
        return jsonify({'error': 'No object name provided'})

if __name__ == '__main__':
    app.run(debug=True)
