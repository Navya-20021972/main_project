import cv2
from ultralytics import YOLO
import os

# Paths
keyframes_dir = "keyframes2"
output_faces_dir = "cropped_faces2"
os.makedirs(output_faces_dir, exist_ok=True)

# Load YOLO face model
model = YOLO("models/best.pt")  # your trained YOLO model

# Process each keyframe
for frame_file in os.listdir(keyframes_dir):
    frame_path = os.path.join(keyframes_dir, frame_file)
    frame = cv2.imread(frame_path)
    if frame is None:
        continue

    # Detect faces
    results = model(frame)

    # Draw boxes and save cropped faces
    for i, box in enumerate(results[0].boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Crop and save face
        face_crop = frame[y1:y2, x1:x2]
        face_path = os.path.join(output_faces_dir, f"{os.path.splitext(frame_file)[0]}_face{i+1}.jpg")
        cv2.imwrite(face_path, face_crop)

    # Show frame with bounding boxes
    cv2.imshow("Keyframe Face Detection", frame)
    key = cv2.waitKey(500)  # display each frame for 500ms
    if key == ord("q"):
        break

cv2.destroyAllWindows()
print(f"Saved cropped faces to {output_faces_dir}")
