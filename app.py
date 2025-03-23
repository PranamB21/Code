from flask import Flask, request, render_template, jsonify
import os
import logging
from skin_tone_analyzer import process_image
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logger.info(f"Created upload folder: {UPLOAD_FOLDER}")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            logger.warning("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            logger.warning("Empty filename in request")
            return jsonify({'error': 'No selected file'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Please upload a PNG, JPG, JPEG, or GIF file.'}), 400
        
        # Read the image file
        image_data = file.read()
        if not image_data:
            logger.warning("Empty image data received")
            return jsonify({'error': 'Empty image file'}), 400
        
        # Process the image
        _, display_data = process_image(image_data)
        
        logger.info("Image processed successfully")
        return jsonify({
            'success': True,
            'display_data': display_data
        })
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the image'}), 500

@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port) 