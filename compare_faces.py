import os
import numpy as np
from scipy.spatial.distance import cosine

EMBEDDINGS_DIR = "embeddings"
THRESHOLD = 0.4  # lower = stricter match

# Load known embeddings
known_embeddings = {}

for file in os.listdir(EMBEDDINGS_DIR):
    if "_" in file and not file.startswith("detected_"):
        name = file.split("_")[0]
        emb = np.load(os.path.join(EMBEDDINGS_DIR, file))
        known_embeddings.setdefault(name, []).append(emb)

# Load detected face embeddings
detected_embeddings = {}

for file in os.listdir(EMBEDDINGS_DIR):
    if file.startswith("detected_"):
        emb = np.load(os.path.join(EMBEDDINGS_DIR, file))
        detected_embeddings[file] = emb

# Compare
for face_file, face_emb in detected_embeddings.items():
    best_match = "UNKNOWN"
    best_score = 1.0

    for person, emb_list in known_embeddings.items():
        for db_emb in emb_list:
            score = cosine(face_emb, db_emb)
            if score < best_score:
                best_score = score
                best_match = person

    if best_score < THRESHOLD:
        print(f"🟢 {face_file} → MATCH: {best_match} (distance={best_score:.3f})")
    else:
        print(f"🔴 {face_file} → UNKNOWN (distance={best_score:.3f})")
