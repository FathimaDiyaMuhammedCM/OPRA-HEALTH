# import os
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torchvision import datasets, transforms, models
# from torch.utils.data import DataLoader
# from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
#
# # ----------------------------
# # Configuration
# # ----------------------------
# DATA_DIR = "C:\\Users\\sivak\\Downloads\\archive (3)"  # Replace with your dataset folder if different
# BATCH_SIZE = 16
# EPOCHS = 10
# LR = 1e-4
# IMG_SIZE = 64  # Resize images
#
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)
#
# # ----------------------------
# # Data transforms
# # ----------------------------
# transform = transforms.Compose([
#     transforms.Resize((IMG_SIZE, IMG_SIZE)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
# ])
#
# # Load datasets
# train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=transform)
# val_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "test"), transform=transform)
#
# train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
# val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
#
# classes = train_dataset.classes
# num_classes = len(classes)
# print("Classes:", classes)
#
# # ----------------------------
# # Model
# # ----------------------------
# # Use a pre-trained model (ResNet18) and replace the classifier
# model = models.resnet18(pretrained=True)
# model.fc = nn.Linear(model.fc.in_features, num_classes)
# model = model.to(device)
#
# # Loss and optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=LR)
#
# # ----------------------------
# # Training loop
# # ----------------------------
# for epoch in range(EPOCHS):
#     model.train()
#     running_loss = 0.0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device)
#
#         optimizer.zero_grad()
#         outputs = model(images)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()
#
#         running_loss += loss.item() * images.size(0)
#
#     epoch_loss = running_loss / len(train_loader.dataset)
#     print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {epoch_loss:.4f}")
#
# # ----------------------------
# # Evaluation
# # ----------------------------
# model.eval()
# all_preds = []
# all_labels = []
#
# with torch.no_grad():
#     for images, labels in val_loader:
#         images, labels = images.to(device), labels.to(device)
#         outputs = model(images)
#         _, preds = torch.max(outputs, 1)
#         all_preds.extend(preds.cpu().numpy())
#         all_labels.extend(labels.cpu().numpy())
#
# # Metrics
# print("Accuracy:", accuracy_score(all_labels, all_preds))
# print("Classification Report:\n", classification_report(all_labels, all_preds, target_names=classes))
# print("Confusion Matrix:\n", confusion_matrix(all_labels, all_preds))
#
# # ----------------------------
# # Save model
# # ----------------------------
# os.makedirs("saved_models", exist_ok=True)
# torch.save(model.state_dict(), "saved_models/facial_emotion_model.pth")
# print("Model saved at saved_models/facial_emotion_model.pth")


import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# Configuration
# ----------------------------
DATA_DIR = r"C:\Users\sivak\Downloads\archive (3)"  # Root dataset folder
BATCH_SIZE = 16
EPOCHS = 10
LR = 1e-4
IMG_SIZE = 64

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ----------------------------
# Data transforms
# ----------------------------
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])

# ----------------------------
# Load datasets
# ----------------------------
train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=transform)
val_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "test"), transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

classes = train_dataset.classes
num_classes = len(classes)
print("Classes:", classes)

# ----------------------------
# Model setup
# ----------------------------
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

# ----------------------------
# Training loop
# ----------------------------
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {epoch_loss:.4f}")

# ----------------------------
# Evaluation
# ----------------------------
model.eval()
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in val_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

# ----------------------------
# Metrics
# ----------------------------
acc = accuracy_score(all_labels, all_preds)
prec = precision_score(all_labels, all_preds, average='weighted', zero_division=0)
rec = recall_score(all_labels, all_preds, average='weighted', zero_division=0)
cm = confusion_matrix(all_labels, all_preds)

print("\n📊 Evaluation Metrics:")
print(f"✅ Accuracy:  {acc:.4f}")
print(f"✅ Precision: {prec:.4f}")
print(f"✅ Recall:    {rec:.4f}\n")

print("📄 Classification Report:\n", classification_report(all_labels, all_preds, target_names=classes))
print("🧩 Confusion Matrix:\n", cm)

# ----------------------------
# Plot confusion matrix
# ----------------------------
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=classes, yticklabels=classes)
plt.title('Confusion Matrix')
plt.xlabel('Predicte d')
plt.ylabel('True')
plt.show()n

# ----------------------------
# Save model
# ----------------------------
os.makedirs("saved_models", exist_ok=True)
torch.save(model.state_dict(), "saved_models/facial_emotion_model.pth")
print("\n💾 Model saved at saved_models/facial_emotion_model.pth")
