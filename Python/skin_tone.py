import cv2
import numpy as np
import stone  # Assuming you have installed the skin-tone-classifier library
import matplotlib.pyplot as plt

def capture_image():
    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

def detect_skin_tone(image):
    # Process the image to detect skin tone
    result = stone.process(image, image_type='color', palette=['#C99676', '#805341', '#9D7A54'], return_report_image=True)
    return result['faces'][0]['skin_tone'], result['faces'][0]['tone_label']

def recommend_colors(skin_tone):
    # Define color recommendations based on skin tone
    recommendations = {
        'CF': ['#C99676', '#E5C8A6', '#F3D1C6'],  # Fair skin
        'CM': ['#805341', '#9D7A54', '#BEA07E'],  # Medium skin
        'CD': ['#6F503C', '#4B3C2A', '#3B2A1D'],  # Dark skin
    }
    return recommendations.get(skin_tone, [])

def display_recommendations(colors):
    # Display recommended colors
    plt.figure(figsize=(8, 4))
    for color in colors:
        plt.fill_between([0, 1], 0, 1, color=color)
    plt.title('Recommended Colors')
    plt.axis('off')
    plt.show()

# Main function
if __name__ == "__main__":
    image = capture_image()
    skin_tone, tone_label = detect_skin_tone(image)
    recommended_colors = recommend_colors(tone_label)
    display_recommendations(recommended_colors)