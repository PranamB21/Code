import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def capture_image():
    # This function will be replaced by file upload in web interface
    pass

def display_image(image, title="Input Image"):
    """
    Convert an image to base64 string for web display
    
    Args:
        image: numpy array (cv2 image)
        title: title for the image
        
    Returns:
        base64 encoded string of the image
    """
    # Convert BGR to RGB for correct color display
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Create figure
    plt.figure(figsize=(8, 6))
    plt.imshow(rgb_image)
    plt.title(title)
    plt.axis('off')
    
    # Save plot to bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def create_analysis_display(image, skin_tone, colors):
    """
    Create a combined display of the input image, skin tone analysis, and color recommendations
    
    Args:
        image: numpy array (cv2 image)
        skin_tone: tuple of (skin tone name, skin tone code)
        colors: list of recommended colors
        
    Returns:
        base64 encoded string of the combined display
    """
    # Create a figure with subplots
    fig = plt.figure(figsize=(15, 8))
    
    # Plot 1: Original Image
    plt.subplot(131)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_image)
    plt.title('Input Image')
    plt.axis('off')
    
    # Plot 2: Skin Tone Analysis
    plt.subplot(132)
    plt.text(0.5, 0.5, f'Skin Tone: {skin_tone[0]}\nCode: {skin_tone[1]}', 
             horizontalalignment='center', verticalalignment='center',
             fontsize=12)
    plt.axis('off')
    
    # Plot 3: Color Recommendations
    plt.subplot(133)
    for i, color in enumerate(colors):
        plt.fill_between([i, i+1], 0, 1, color=color)
    plt.xlim(0, len(colors))
    plt.title('Recommended Colors')
    plt.axis('off')
    
    # Adjust layout and save
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

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
        # Convert to RGB color space for additional analysis
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except cv2.error as e:
        raise ValueError(f"Failed to convert image color spaces: {str(e)}. Please ensure the image is in BGR format")
    
    # Calculate average HSV and RGB values
    hsv_avg = np.mean(hsv_image, axis=(0, 1))
    rgb_avg = np.mean(rgb_image, axis=(0, 1))
    
    # Calculate additional metrics
    saturation = hsv_avg[1]
    value = hsv_avg[2]
    red_ratio = rgb_avg[0] / (rgb_avg[0] + rgb_avg[1] + rgb_avg[2])
    
    # Enhanced skin tone classification with more categories
    if saturation < 25 and value > 220:  # Very fair skin
        return "Very Light", "VLF"
    elif saturation < 35 and value > 200:  # Fair skin
        return "Fair", "F"
    elif saturation < 45 and value > 180:  # Light skin
        return "Light", "L"
    elif saturation < 55 and value > 160:  # Light Medium skin
        return "Light Medium", "LM"
    elif saturation < 65 and value > 140:  # Medium skin
        return "Medium", "M"
    elif saturation < 75 and value > 120:  # Medium Dark skin
        return "Medium Dark", "MD"
    elif saturation < 85 and value > 100:  # Dark skin
        return "Dark", "D"
    elif saturation < 95 and value > 80:  # Deep skin
        return "Deep", "DP"
    else:  # Very Deep skin
        return "Very Deep", "VD"

def recommend_colors(skin_tone):
    # Enhanced color recommendations based on skin tone
    recommendations = {
        'VLF': [
            '#F5E6E8', '#FADBD8', '#F5B7B1', '#F1948A', '#EC7063', '#E74C3C',
            '#F8C471', '#F39C12', '#D35400'
        ],  # Very fair skin
        'F': [
            '#C99676', '#E5C8A6', '#F3D1C6', '#F5B7B1', '#FAD7A1', '#F9E79F',
            '#F1C40F', '#F39C12', '#D35400'
        ],  # Fair skin
        'L': [
            '#D5BDAF', '#C39BD3', '#A3E4D7', '#76D7C4', '#48C9B0', '#1ABC9C',
            '#3498DB', '#2980B9', '#2472A4'
        ],  # Light skin
        'LM': [
            '#805341', '#9D7A54', '#BEA07E', '#D5BDAF', '#C39BD3', '#A3E4D7',
            '#3498DB', '#2980B9', '#2472A4'
        ],  # Light medium skin
        'M': [
            '#6F503C', '#4B3C2A', '#3B2A1D', '#A569BD', '#F1948A', '#F7DC6F',
            '#E74C3C', '#C0392B', '#A93226'
        ],  # Medium skin
        'MD': [
            '#4B3C2A', '#3B2A1D', '#A569BD', '#F1948A', '#F7DC6F', '#F4D03F',
            '#E74C3C', '#C0392B', '#A93226'
        ],  # Medium dark skin
        'D': [
            '#2C3E50', '#34495E', '#2C3E50', '#A569BD', '#F1948A', '#F7DC6F',
            '#E74C3C', '#C0392B', '#A93226'
        ],  # Dark skin
        'DP': [
            '#1A252F', '#2C3E50', '#34495E', '#A569BD', '#F1948A', '#F7DC6F',
            '#E74C3C', '#C0392B', '#A93226'
        ],  # Deep skin
        'VD': [
            '#17202A', '#1A252F', '#2C3E50', '#A569BD', '#F1948A', '#F7DC6F',
            '#E74C3C', '#C0392B', '#A93226'
        ]  # Very Deep skin
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
        tuple of (cv2 image, display data)
    """
    try:
        if isinstance(image_data, str):  # File path
            image = cv2.imread(image_data)
        elif isinstance(image_data, bytes):  # Bytes data
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            # Decode the numpy array as an image
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif isinstance(image_data, np.ndarray):  # Already a cv2 image
            image = image_data.copy()  # Make a copy to avoid modifying original
        else:
            raise ValueError("Unsupported image format")
            
        if image is None:
            raise ValueError("Failed to load image")
            
        # Ensure image is in BGR format and correct shape
        if len(image.shape) != 3:
            raise ValueError("Image must be a color image with 3 channels")
            
        if image.shape[2] != 3:
            raise ValueError("Image must have 3 color channels (BGR)")
            
        # Get skin tone analysis
        skin_tone = detect_skin_tone(image)
        colors = recommend_colors(skin_tone[1])
        
        # Create display data
        display_data = create_analysis_display(image, skin_tone, colors)
            
        return image, display_data
        
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")