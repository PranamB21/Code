from flask import Flask, request, render_template, jsonify
import os
import shutil
from datetime import datetime, timedelta
from skin_tone_analyzer import process_image

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def cleanup_old_files():
    """Remove files older than 24 hours from the uploads directory"""
    cutoff = datetime.now() - timedelta(hours=24)
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            if datetime.fromtimestamp(os.path.getctime(filepath)) < cutoff:
                os.remove(filepath)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file type. Please upload a PNG, JPG, JPEG, or GIF file.'}), 400
    
    # Validate file size (max 5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': f'File size exceeds maximum limit of 5MB'}), 400
    
    # Read the image file
    try:
        image_data = file.read()
        if not image_data:
            return jsonify({'error': 'Empty image file'}), 400
        
        # Process the image
        _, display_data = process_image(image_data)
        
        # Clean up uploaded file from memory
        file.close()
        
        return jsonify({
            'success': True,
            'display_data': display_data
        })
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)