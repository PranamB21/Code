from flask import Flask, request, render_template, jsonify
import os
from skin_tone import process_image
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Read the image file
        image_data = file.read()
        
        # Process the image
        _, display_data = process_image(image_data)
        
        return jsonify({
            'success': True,
            'display_data': display_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use PORT environment variable if available
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 