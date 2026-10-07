import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

# ----------------------------
# Configuration
# ----------------------------
MODEL_PATH = "saved_models/facial_emotion_model.pth"
IMG_SIZE = 64  # Same as training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Classes (must match your dataset)
# ----------------------------
classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
num_classes = len(classes)

# ----------------------------
# Data transforms
# ----------------------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# ----------------------------
# Load trained model
# ----------------------------
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model = model.to(device)
model.eval()

# ----------------------------
# Prediction function
# ----------------------------
def predict_emotion(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)  # Add batch dimension

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1).cpu().numpy().flatten()
        pred_class = classes[probs.argmax()]

    return pred_class, probs

# ----------------------------
# Example usage

# ----------------------------
if __name__ == "__main__":
    # Change this path to any image you want to test
    test_image = r"C:\Users\sivak\Downloads\archive (3)\test\fear\PublicTest_92576393.jpg"

    predicted_emotion, probabilities = predict_emotion(test_image)
    print(f"\n🧩 Predicted Emotion: {predicted_emotion}\n")
    print("📊 Probabilities:")
    for cls, prob in zip(classes, probabilities):
        print(f"{cls:10s}: {prob:.4f}")
