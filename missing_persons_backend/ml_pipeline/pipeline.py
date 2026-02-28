"""
ML Pipeline wrapper for integrating your existing Python scripts
with the Django backend
"""

import cv2
import numpy as np
from pathlib import Path
from django.conf import settings

class FacialRecognitionPipeline:
    """
    Wrapper for your ML pipeline
    """
    
    def __init__(self):
        try:
            from ultralytics import YOLO
            from deepface import DeepFace
            self.YOLO = YOLO
            self.DeepFace = DeepFace
            self.model_loaded = True
            self.face_model = None
        except ImportError:
            self.model_loaded = False
            print("Warning: Required ML libraries not installed")
    
    def load_face_detection_model(self):
        """Load YOLO face detection model"""
        try:
            model_path = settings.FACE_DETECTION_MODEL
            if Path(model_path).exists():
                self.face_model = self.YOLO(str(model_path))
                return True
        except Exception as e:
            print(f"Error loading face detection model: {e}")
        return False
    
    def extract_keyframes(self, video_path, num_keyframes=10):
        """
        Extract keyframes from video
        Can integrate your genetic algorithm later
        """
        try:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            keyframe_indices = np.linspace(0, total_frames-1, num_keyframes, dtype=int)
            keyframes = []
            
            for idx in keyframe_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    keyframes.append(frame)
            
            cap.release()
            return keyframes
        except Exception as e:
            print(f"Error extracting keyframes: {e}")
            return []
    
    def detect_faces(self, frame):
        """
        Detect faces in a frame using YOLO
        Returns list of face crops and coordinates
        """
        if not self.face_model:
            self.load_face_detection_model()
        
        try:
            results = self.face_model(frame)
            faces = []
            
            for box in results[0].boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                face_crop = frame[y1:y2, x1:x2]
                faces.append({
                    'crop': face_crop,
                    'coords': (x1, y1, x2, y2)
                })
            
            return faces
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def generate_embedding(self, face_image):
        """
        Generate face embedding from image (from file path)
        """
        try:
            embedding = self.DeepFace.represent(
                img_path=face_image,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False
            )[0]["embedding"]
            return np.array(embedding)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def generate_embedding_cv2(self, face_image_array):
        """
        Generate face embedding from OpenCV image array
        """
        try:
            # Convert BGR to RGB
            if len(face_image_array.shape) == 3:
                face_rgb = cv2.cvtColor(face_image_array, cv2.COLOR_BGR2RGB)
            else:
                face_rgb = face_image_array
            
            embedding = self.DeepFace.represent(
                img_path=face_rgb,
                model_name="Facenet",
                detector_backend="skip",
                enforce_detection=False
            )[0]["embedding"]
            return np.array(embedding)
        except Exception as e:
            print(f"Error generating embedding from array: {e}")
            return None
    
    def compare_embeddings(self, embedding1, embedding2):
        """
        Compare two embeddings using cosine distance
        Returns confidence score (0-1, higher is better match)
        """
        try:
            from scipy.spatial.distance import cosine
            distance = cosine(embedding1, embedding2)
            # Convert distance to confidence (0 distance = 1.0 confidence)
            confidence = 1 - distance
            return max(0, min(1, confidence))
        except Exception as e:
            print(f"Error comparing embeddings: {e}")
            return 0.0


# Initialize pipeline instance
ml_pipeline = FacialRecognitionPipeline()
