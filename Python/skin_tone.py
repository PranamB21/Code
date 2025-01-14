import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def capture_image():
    # This function will be replaced by file upload in web interface
    pass

def detect_skin_tone(image):
    # Input validation
    if image is None:
        raise ValueError("No image provided")
    
    if not isinstance(image, np.ndarray):
        raise TypeError("Input must be a numpy array (cv2 image)")
        
    # Check if image is empty
    if image.size == 0:
        raise ValueError("Empty image provided")
        
    # Check if image has valid dimensions
    if len(image.shape) != 3:
        raise ValueError("Image must be a color image with 3 channels")
    
    try:
        # Convert to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    except cv2.error:
        raise ValueError("Failed to convert image to HSV color space. Please ensure the image is in BGR format")
    
    # Calculate average HSV values in the image
    average_color = np.mean(hsv_image, axis=(0, 1))
    
    # Define more detailed skin tone ranges
    if average_color[1] < 30 and average_color[2] > 200:  # Very fair skin
        return "Very Light", "VLF"
    elif average_color[1] < 50:  # Fair skin
        return "Light", "LF"
    elif average_color[1] < 70:  # Light medium skin
        return "Light Medium", "LM"
    elif average_color[1] < 100:  # Medium skin
        return "Medium", "MF"
    elif average_color[1] < 130:  # Medium dark skin
        return "Medium Dark", "MD"
    else:  # Dark skin
        return "Dark", "DF"

def recommend_colors(skin_tone):
    # Define color recommendations based on skin tone
    recommendations = {
        'VLF': [
            '#F5E6E8', '#FADBD8', '#F5B7B1', '#F1948A', '#EC7063', '#E74C3C'
        ],  # Very fair skin
        'LF': [
            '#C99676', '#E5C8A6', '#F3D1C6', '#F5B7B1', '#FAD7A1', '#F9E79F'
        ],  # Fair skin
        'LM': [
            '#D5BDAF', '#C39BD3', '#A3E4D7', '#76D7C4', '#48C9B0', '#1ABC9C'
        ],  # Light medium skin
        'MF': [
            '#805341', '#9D7A54', '#BEA07E', '#D5BDAF', '#C39BD3', '#A3E4D7'
        ],  # Medium skin
        'MD': [
            '#6F503C', '#4B3C2A', '#3B2A1D', '#A569BD', '#F1948A', '#F7DC6F'
        ],  # Medium dark skin
        'DF': [
            '#4B3C2A', '#3B2A1D', '#A569BD', '#F1948A', '#F7DC6F', '#F4D03F'
        ],  # Dark skin
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

def generate_colors(base_color, num_colors=5):
    # Convert hex to RGB
    base_rgb = [int(base_color[i:i+2], 16) for i in (1, 3, 5)]
    colors = []
    
    for i in range(num_colors):
        # Generate a new color by modifying the base color with a more varied approach
        new_color = [
            (base_rgb[j] + (i * 30) + (i * 10) % 256) % 256 for j in range(3)
        ]
        colors.append('#{:02x}{:02x}{:02x}'.format(*new_color))
    
    return colors

def process_image(image_data):
    """
    Process the input image data and convert it to cv2 format
    
    Args:
        image_data: Can be a file path, bytes, or numpy array
        
    Returns:
        cv2 image (numpy array)
    """
    try:
        if isinstance(image_data, str):  # File path
            image = cv2.imread(image_data)
        elif isinstance(image_data, bytes):  # Bytes data
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif isinstance(image_data, np.ndarray):  # Already a cv2 image
            image = image_data
        else:
            raise ValueError("Unsupported image format")
            
        if image is None:
            raise ValueError("Failed to load image")
            
        return image
        
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")