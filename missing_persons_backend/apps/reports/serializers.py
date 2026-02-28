from rest_framework import serializers
from .models import Location, Camera, Report, CameraVideo, SearchResult

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 'created_at']

class CameraSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = Camera
        fields = ['id', 'name', 'location', 'location_name', 'description', 'is_active']

class CameraVideoSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    
    class Meta:
        model = CameraVideo
        fields = ['id', 'camera', 'camera_name', 'video_file', 'recording_date', 'duration']

class ReportSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='last_seen_location.name', read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.get_full_name', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'missing_person_name', 'missing_person_photo', 
            'description', 'last_seen_location', 'location_name',
            'last_seen_time', 'reported_by', 'reported_by_name',
            'status', 'created_at', 'updated_at'
        ]

class ReportDetailSerializer(ReportSerializer):
    class Meta(ReportSerializer.Meta):
        fields = ReportSerializer.Meta.fields + ['id']

class SearchResultSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    location_name = serializers.CharField(source='camera.location.name', read_only=True)
    
    class Meta:
        model = SearchResult
        fields = [
            'id', 'report', 'camera', 'camera_name', 'location_name',
            'video', 'match_time', 'confidence', 'confidence_level',
            'face_snapshot', 'created_at'
        ]
