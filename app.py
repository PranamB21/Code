from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
from Python.skin_tone import detect_skin_tone, recommend_colors, create_color_preview

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    # Check if the file has a name
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Check if the file is allowed
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'error': 'Invalid file type. Please upload a PNG, JPG, or GIF image'}), 400
    
    try:
        # Read and process the uploaded image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Failed to process image. Please try another image.'}), 400
            
        # Process the image
        processed_image = process_image(image)  # Use the image directly since it's already in cv2 format
        skin_tone, tone_label = detect_skin_tone(processed_image)
        recommended_colors = recommend_colors(tone_label)
        color_preview = create_color_preview(recommended_colors)
        
        return jsonify({
            'skin_tone': skin_tone,
            'tone_label': tone_label,
            'recommended_colors': recommended_colors,
            'color_preview': color_preview
        })
        
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")  # Add proper logging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Disable debug mode in production
 