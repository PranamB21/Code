# Training Data Directory Structure

This directory should contain skin tone image samples organized in the following categories:

- VLF (Very Light Fair)
- F (Fair)
- L (Light)
- LM (Light Medium)
- M (Medium)
- MD (Medium Dark)
- D (Dark)
- DP (Dark Plus)
- VD (Very Dark)

Please organize your training images in the following structure:

```
training_data/
  ├── VLF/
  │   ├── image1.jpg
  │   └── image2.jpg
  ├── F/
  │   ├── image1.jpg
  │   └── image2.jpg
  └── ...
```

Each image should be in JPG, JPEG, or PNG format.
The model expects facial images for accurate skin tone classification.