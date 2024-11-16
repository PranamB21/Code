from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
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
    # Read and process the uploaded image
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    try:
        skin_tone, tone_label = detect_skin_tone(image)
        recommended_colors = recommend_colors(tone_label)
        color_preview = create_color_preview(recommended_colors)
        
        return jsonify({
            'skin_tone': skin_tone,
            'tone_label': tone_label,
            'recommended_colors': recommended_colors,
            'color_preview': color_preview
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 