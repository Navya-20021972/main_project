import os
import numpy as np
from deepface import DeepFace

# Paths
cropped_faces_dir = "cropped_faces2"
face_db_dir = "face_db"  # DB of known people

# Create embeddings folder
os.makedirs("embeddings", exist_ok=True)

# ==============================
# STEP 1: Embeddings for KNOWN people (DB)
# ==============================
for person in os.listdir(face_db_dir):
    person_folder = os.path.join(face_db_dir, person)

    if not os.path.isdir(person_folder):
        continue

    for img_file in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_file)

        try:
            embedding = DeepFace.represent(
                img_path=img_path,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False
            )[0]["embedding"]

            emb_path = os.path.join("embeddings", f"{person}_{img_file}.npy")
            np.save(emb_path, embedding)

            print(f"✅ Saved embedding: {emb_path}")

        except Exception as e:
            print(f"❌ Failed on {img_path}: {e}")

# ==============================
# STEP 2: Embeddings for DETECTED faces
# ==============================
detected_embeddings = {}

for img_file in os.listdir(cropped_faces_dir):
    img_path = os.path.join(cropped_faces_dir, img_file)

    try:
        embedding = DeepFace.represent(
            img_path=img_path,
            model_name="Facenet",
            detector_backend="skip",
            enforce_detection=False
        )[0]["embedding"]

        np.save(os.path.join("embeddings", f"detected_{img_file}.npy"), embedding)

        print(f"✅ Embedded detected face: {img_file}")

    except Exception as e:
        print(f"❌ Failed on {img_path}: {e}")

print("\n🎉 Embeddings generated for DB and detected faces!")
