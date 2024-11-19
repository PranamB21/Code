import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def capture_image():
    # This function will be replaced by file upload in web interface
    pass

def detect_skin_tone(image):
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate average HSV values in the image
    average_color = np.mean(hsv_image, axis=(0, 1))
    
    # Define skin tone ranges (these are approximate values)
    if average_color[1] < 50:  # Low saturation indicates fair skin
        return "Light", "CF"
    elif average_color[1] < 100:  # Medium saturation indicates medium skin
        return "Medium", "CM"
    else:  # High saturation indicates darker skin
        return "Dark", "CD"

def recommend_colors(skin_tone):
    # Define color recommendations based on skin tone
    recommendations = {
        'CF': ['#C99676', '#E5C8A6', '#F3D1C6'],  # Fair skin
        'CM': ['#805341', '#9D7A54', '#BEA07E'],  # Medium skin
        'CD': ['#6F503C', '#4B3C2A', '#3B2A1D'],  # Dark skin
    }
    return recommendations.get(skin_tone, [])

def create_color_preview(colors):
    # Create color preview image for web display
    plt.figure(figsize=(8, 4))
    for i, color in enumerate(colors):
        plt.fill_between([i, i+1], 0, 1, color=color)
    plt.xlim(0, len(colors))
    plt.title('Recommended Colors')
    plt.axis('off')
    
    # Save plot to bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

print(dir(stone))