import os
from PIL import Image
import random

# Parameters
base_dir = "captured_faces"
split_dirs = ["train", "val"]
emotions = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
images_per_class = 20  # synthetic images per class

# Create folders
for split in split_dirs:
    for emotion in emotions:
        os.makedirs(os.path.join(base_dir, split, emotion), exist_ok=True)

# Generate dummy images
for split in split_dirs:
    for emotion in emotions:
        folder = os.path.join(base_dir, split, emotion)
        for i in range(images_per_class):
            img = Image.new('RGB', (64, 64), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            img.save(os.path.join(folder, f"{emotion}_{i}.jpg"))

print("Synthetic folder dataset created successfully!")
