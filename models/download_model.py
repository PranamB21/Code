import os
import requests
import torch

def download_model():
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Model file path
    model_path = os.path.join('models', 'skin_tone_classifier.pth')
    
    # Skip if model already exists
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        return
    
    # Download model from the repository
    model_url = "https://github.com/ChenglongMa/SkinToneClassifier/raw/main/models/skin_tone_classifier.pth"
    try:
        response = requests.get(model_url)
        response.raise_for_status()
        
        # Save the model
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded model to {model_path}")
        
    except Exception as e:
        print(f"Error downloading model: {str(e)}")

if __name__ == "__main__":
    download_model()