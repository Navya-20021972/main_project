import cv2
import numpy as np
from ultralytics import YOLO
import os
import random
from deepface import DeepFace
from scipy.spatial.distance import cosine

# ----------------------
# SETTINGS
# ----------------------
video_path = r"C:data\videos\vid3.mp4"  # your video
output_frames_dir = "keyframes2"
output_faces_dir = "cropped_faces2"
face_db_dir = "face_db"  # folder with subfolders for known people

population_size = 20
generations = 5
mutation_rate = 0.1
num_keyframes = 10
THRESHOLD = 0.4  # cosine distance threshold for a match

# YOLO face model
model = YOLO(r"models/best.pt")

# ----------------------
# UTILITY FUNCTIONS
# ----------------------
def frame_difference_score(f1, f2):
    h1 = cv2.calcHist([f1], [0,1,2], None, [8,8,8], [0,256]*3)
    h2 = cv2.calcHist([f2], [0,1,2], None, [8,8,8], [0,256]*3)
    cv2.normalize(h1,h1)
    cv2.normalize(h2,h2)
    return cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)

def mutate(candidate, total_frames):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(candidate)-1)
        candidate[idx] = random.randint(0, total_frames-1)
    return candidate

def fitness(candidate, all_frames):
    score = 0
    for i in range(len(candidate)-1):
        f1 = all_frames[candidate[i]]
        f2 = all_frames[candidate[i+1]]
        score += 1 - frame_difference_score(f1, f2)
    return score

# ----------------------
# LOAD VIDEO FRAMES
# ----------------------
if not os.path.exists(video_path):
    print("❌ Video not found!")
    exit()

cap = cv2.VideoCapture(video_path)
all_frames = []
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    all_frames.append(frame)
    frame_count += 1
cap.release()
print(f"Loaded {frame_count} frames from video.")

if frame_count == 0:
    print("❌ Video has no frames.")
    exit()

# ----------------------
# ADJUST NUM_KEYFRAMES
# ----------------------
if frame_count < num_keyframes:
    num_keyframes = frame_count

# ----------------------
# GA TO SELECT KEYFRAMES
# ----------------------
population = [random.sample(range(frame_count), num_keyframes) for _ in range(population_size)]

for gen in range(generations):
    fitness_scores = [fitness(cand, all_frames) for cand in population]
    sorted_pop = [c for _,c in sorted(zip(fitness_scores,population), reverse=True)]
    population = sorted_pop[:population_size//2]
    new_population = []
    while len(new_population) < population_size:
        parents = random.sample(population, 2)
        cross_point = random.randint(1, num_keyframes-1)
        child = parents[0][:cross_point] + parents[1][cross_point:]
        child = mutate(child, frame_count)
        new_population.append(child)
    population = new_population

best_candidate = sorted(population, key=lambda c: fitness(c, all_frames), reverse=True)[0]
keyframes = sorted(best_candidate)
print(f"Selected {len(keyframes)} keyframes.")

# ----------------------
# CREATE OUTPUT FOLDERS
# ----------------------
os.makedirs(output_frames_dir, exist_ok=True)
os.makedirs(output_faces_dir, exist_ok=True)

# ----------------------
# GENERATE KNOWN FACE EMBEDDINGS
# ----------------------
known_embeddings = {}

for person in os.listdir(face_db_dir):
    person_folder = os.path.join(face_db_dir, person)
    if not os.path.isdir(person_folder):
        continue
    for img_file in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_file)
        try:
            emb = DeepFace.represent(
                img_path=img_path,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False
            )[0]["embedding"]
            known_embeddings.setdefault(person, []).append(emb)
        except Exception as e:
            print(f"❌ Failed on {img_path}: {e}")

print("✅ Known face embeddings loaded.")

# ----------------------
# PROCESS KEYFRAMES + LIVE DETECTION + MATCHING
# ----------------------
for i, idx in enumerate(keyframes):
    frame = all_frames[idx]
    results = model(frame)

    for j, box in enumerate(results[0].boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)
        face_crop = frame[y1:y2, x1:x2]
        face_path = os.path.join(output_faces_dir, f"frame{i+1}_face{j+1}.jpg")
        cv2.imwrite(face_path, face_crop)

        # ----------------------
        # DETECTED FACE EMBEDDING
        # ----------------------
        try:
            det_emb = DeepFace.represent(
                img_path=face_path,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False
            )[0]["embedding"]
        except Exception as e:
            print(f"❌ Failed embedding for {face_path}: {e}")
            continue

        # ----------------------
        # COMPARE WITH KNOWN EMBEDDINGS
        # ----------------------
        best_match = "UNKNOWN"
        best_score = 1.0
        for person, emb_list in known_embeddings.items():
            for db_emb in emb_list:
                score = cosine(det_emb, db_emb)
                if score < best_score:
                    best_score = score
                    best_match = person

        if best_score < THRESHOLD:
            print(f"🟢 {face_path} → MATCH: {best_match} (distance={best_score:.3f})")
        else:
            print(f"🔴 {face_path} → UNKNOWN (distance={best_score:.3f})")

    # Show live frame with red boxes
    cv2.imshow("Face Detection Live", frame)
    key = cv2.waitKey(100)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
print("🎉 Pipeline complete: keyframes saved, faces cropped, embeddings matched.")