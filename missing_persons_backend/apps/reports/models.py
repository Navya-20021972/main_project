from django.db import models
from apps.users.models import User

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Camera(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cameras')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.location.name})"
    
    class Meta:
        unique_together = ['name', 'location']
        ordering = ['location', 'name']


class Report(models.Model):
    STATUS_CHOICES = [
        ('filed', 'Filed'),
        ('searching', 'Searching'),
        ('found', 'Found'),
        ('closed', 'Closed'),
    ]
    
    missing_person_name = models.CharField(max_length=200)
    missing_person_photo = models.ImageField(upload_to='missing_persons/')
    description = models.TextField()
    last_seen_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    last_seen_time = models.DateTimeField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='filed')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report: {self.missing_person_name} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']


class CameraVideo(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='camera_videos/')
    recording_date = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in seconds")
    is_processed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.camera.name} - {self.recording_date}"
    
    class Meta:
        ordering = ['-recording_date']


class SearchResult(models.Model):
    CONFIDENCE_LEVEL = [
        ('high', 'High Confidence (>90%)'),
        ('medium', 'Medium Confidence (70-90%)'),
        ('low', 'Low Confidence (<70%)'),
    ]
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='search_results')
    camera = models.ForeignKey(Camera, on_delete=models.PROTECT)
    video = models.ForeignKey(CameraVideo, on_delete=models.PROTECT)
    
    match_time = models.DateTimeField()
    confidence = models.FloatField()  # 0-1
    confidence_level = models.CharField(max_length=10, choices=CONFIDENCE_LEVEL)
    
    face_snapshot = models.ImageField(upload_to='matched_faces/')
    embedding = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Match: {self.report.missing_person_name} at {self.camera.name}"
    
    class Meta:
        ordering = ['-created_at']
