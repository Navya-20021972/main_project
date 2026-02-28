from rest_framework import serializers
from .models import SearchJob
from apps.reports.serializers import SearchResultSerializer

class SearchJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchJob
        fields = [
            'id', 'report', 'status', 'progress', 'matches_found',
            'videos_processed', 'total_videos', 'created_at', 'started_at',
            'completed_at', 'error_message'
        ]
        read_only_fields = ['progress', 'matches_found', 'videos_processed']
