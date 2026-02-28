import cv2
from ultralytics import YOLO
import os

# Loal# or whichever YOLO face model you use
model = YOLO("models/best.pt")

# Load image
img_path = "data/user/user2.jpeg"
img = cv2.imread(img_path)

# Create output folder
output_dir = "cropped_faces"
os.makedirs(output_dir, exist_ok=True)

# Run detection
results = model(img)

# Loop through detections
for i, result in enumerate(results[0].boxes.xyxy):  # xyxy boxes
    x1, y1, x2, y2 = map(int, result)
    face_crop = img[y1:y2, x1:x2]
    cv2.imwrite(f"{output_dir}/face_{i+1}.jpg", face_crop)

print(f"Cropped {len(results[0].boxes)} faces to {output_dir}")
