import os
import kagglehub
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from PIL import Image

def load_and_preprocess_data(dataset_path):
    images = []
    labels = []
    
    # Load images and preprocess
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path)
                    img = img.resize((224, 224))  # Resize to standard size
                    img_array = np.array(img) / 255.0  # Normalize
                    images.append(img_array)
                    
                    # Extract label from directory name
                    label = os.path.basename(root)
                    labels.append(label)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
    
    return np.array(images), np.array(labels)

def create_model(num_classes):
    model = models.Sequential([
        layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def main():
    # Download dataset
    print("Downloading dataset...")
    dataset_path = kagglehub.dataset_download("ducnguyen168/dataset-skin-tone")
    print(f"Dataset downloaded to: {dataset_path}")
    
    # Load and preprocess data
    print("Loading and preprocessing data...")
    X, y = load_and_preprocess_data(dataset_path)
    
    # Convert labels to numerical format
    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Create and compile model
    num_classes = len(np.unique(y))
    model = create_model(num_classes)
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Train model
    print("Training model...")
    history = model.fit(X_train, y_train,
                       epochs=10,
                       validation_data=(X_test, y_test),
                       batch_size=32)
    
    # Save model
    model.save('skin_tone_model.h5')
    print("Model saved as 'skin_tone_model.h5'")
    
    # Evaluate model
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"\nTest accuracy: {test_acc:.4f}")

if __name__ == "__main__":
    main()