import os
import kagglehub
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
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

class SkinToneModel(nn.Module):
    def __init__(self, num_classes):
        super(SkinToneModel, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 64, 3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 26 * 26, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
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
    
    # Convert to PyTorch tensors
    X_train = torch.FloatTensor(X_train).permute(0, 3, 1, 2)
    X_test = torch.FloatTensor(X_test).permute(0, 3, 1, 2)
    y_train = torch.LongTensor(y_train)
    y_test = torch.LongTensor(y_test)
    
    # Create model
    num_classes = len(np.unique(y))
    model = SkinToneModel(num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    
    # Train model
    print("Training model...")
    num_epochs = 10
    batch_size = 32
    
    for epoch in range(num_epochs):
        model.train()
        for i in range(0, len(X_train), batch_size):
            batch_X = X_train[i:i+batch_size].to(device)
            batch_y = y_train[i:i+batch_size].to(device)
            
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
        
        # Evaluate
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test.to(device))
            _, predicted = torch.max(test_outputs.data, 1)
            accuracy = (predicted == y_test.to(device)).sum().item() / len(y_test)
            print(f'Epoch [{epoch+1}/{num_epochs}], Test Accuracy: {accuracy:.4f}')
    
    # Save model
    torch.save(model.state_dict(), 'skin_tone_model.pth')
    print("Model saved as 'skin_tone_model.pth'")
    
    # Final evaluation
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test.to(device))
        _, predicted = torch.max(test_outputs.data, 1)
        final_accuracy = (predicted == y_test.to(device)).sum().item() / len(y_test)
        print(f"\nFinal Test Accuracy: {final_accuracy:.4f}")

if __name__ == "__main__":
    main()