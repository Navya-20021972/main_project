from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import SearchJob
from .serializers import SearchJobSerializer
from apps.reports.models import Report, SearchResult, CameraVideo
import os
import tempfile
from datetime import datetime

# Import ML pipeline - may fail if openCV/deepface not installed
try:
    from ml_pipeline.pipeline import ml_pipeline
    import cv2
    import numpy as np
    ML_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    ML_AVAILABLE = False
    ml_pipeline = None


class SearchJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for search jobs.
    """
    queryset = SearchJob.objects.all()
    serializer_class = SearchJobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SearchJob.objects.all().order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def start_search(self, request):
        """
        Start a facial recognition search.
        
        Request body:
        {
            "report_id": 1,
            "camera_ids": [1, 2, 3]
        }
        """
        if not ML_AVAILABLE:
            return Response(
                {'error': 'ML pipeline not available. Please install opencv-python and deepface.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        report_id = request.data.get('report_id')
        camera_ids = request.data.get('camera_ids', [])
        
        if not report_id:
            return Response(
                {'error': 'report_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create search job
        search_job = SearchJob.objects.create(
            report=report,
            status='processing',
            started_at=timezone.now()
        )
        
        # Add cameras to job
        if camera_ids:
            search_job.cameras.set(camera_ids)
        
        # Get videos for selected cameras
        videos = CameraVideo.objects.filter(camera_id__in=camera_ids) if camera_ids else CameraVideo.objects.all()
        search_job.total_videos = videos.count()
        search_job.save()
        
        # TODO: In production, this should be a Celery task
        # For now, process synchronously for demo
        try:
            self._process_search(search_job, report, videos)
        except Exception as e:
            search_job.status = 'failed'
            search_job.error_message = str(e)
            search_job.save()
        
        serializer = SearchJobSerializer(search_job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _process_search(self, search_job, report, videos):
        """
        Process videos and perform facial recognition.
        """
        # Generate embedding for missing person photo
        report_embedding = None
        if report.missing_person_photo:
            try:
                # Save temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    for chunk in report.missing_person_photo.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name
                
                report_embedding = ml_pipeline.generate_embedding(tmp_path)
                os.unlink(tmp_path)
            except Exception as e:
                print(f"Error generating embedding for report: {e}")
        
        if not report_embedding:
            search_job.status = 'failed'
            search_job.error_message = 'Could not generate embedding for missing person photo'
            search_job.save()
            return
        
        # Process each video
        for idx, video in enumerate(videos):
            try:
                self._process_video(search_job, report, video, report_embedding)
                search_job.videos_processed += 1
            except Exception as e:
                print(f"Error processing video {video.id}: {e}")
            
            # Update progress
            progress = int((search_job.videos_processed / search_job.total_videos) * 100)
            search_job.progress = progress
            search_job.save()
        
        # Mark as completed
        search_job.status = 'completed'
        search_job.completed_at = timezone.now()
        search_job.save()
    
    def _process_video(self, search_job, report, video, report_embedding):
        """
        Process a single video file.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            for chunk in video.video_file.chunks():
                tmp.write(chunk)
            video_path = tmp.name
        
        try:
            # Extract keyframes
            keyframes = ml_pipeline.extract_keyframes(video_path, num_keyframes=5)
            
            for keyframe_idx, keyframe in enumerate(keyframes):
                # Detect faces
                faces = ml_pipeline.detect_faces(keyframe)
                
                for face_data in faces:
                    face_crop = face_data['crop']
                    
                    # Generate embedding
                    face_embedding = ml_pipeline.generate_embedding_cv2(face_crop)
                    if not face_embedding:
                        continue
                    
                    # Compare embeddings
                    confidence = ml_pipeline.compare_embeddings(report_embedding, face_embedding)
                    
                    # If match confidence is high enough, save result
                    if confidence > 0.4:  # Using THRESHOLD from settings
                        # Convert confidence to level
                        if confidence > 0.9:
                            confidence_level = 'high'
                        elif confidence > 0.7:
                            confidence_level = 'medium'
                        else:
                            confidence_level = 'low'
                        
                        # Save face snapshot
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir=None) as tmp_img:
                            cv2.imwrite(tmp_img.name, face_crop)
                            
                            # Create search result
                            from django.core.files import File
                            with open(tmp_img.name, 'rb') as img_file:
                                result = SearchResult.objects.create(
                                    report=report,
                                    camera=video.camera,
                                    video=video,
                                    match_time=timezone.now(),
                                    confidence=confidence,
                                    confidence_level=confidence_level,
                                    embedding=face_embedding.tolist() if isinstance(face_embedding, np.ndarray) else face_embedding
                                )
                                result.face_snapshot.save(
                                    f'result_{result.id}.jpg',
                                    File(img_file)
                                )
                                result.save()
                                search_job.matches_found += 1
                            
                            os.unlink(tmp_img.name)
        finally:
            os.unlink(video_path)

