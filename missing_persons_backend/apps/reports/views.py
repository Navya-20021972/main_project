from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Location, Camera, Report, CameraVideo, SearchResult
from .serializers import (
    LocationSerializer, CameraSerializer, ReportSerializer,
    ReportDetailSerializer, CameraVideoSerializer, SearchResultSerializer
)


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Location.objects.all().order_by('name')


class CameraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cameras to be viewed or edited.
    """
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        location_id = self.request.query_params.get('location_id')
        if location_id:
            return Camera.objects.filter(location_id=location_id)
        return Camera.objects.all()


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for missing person reports.
    """
    queryset = Report.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        """
        Allow unauthenticated users to create reports.
        Require authentication for other actions.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReportDetailSerializer
        return ReportSerializer
    
    def get_queryset(self):
        # Users can see their own reports, admins see all
        user = self.request.user
        if user and user.is_authenticated:
            if user.role == 'admin':
                return Report.objects.all()
            return Report.objects.filter(reported_by=user)
        # Unauthenticated users can't view reports
        return Report.objects.none()
    
    def perform_create(self, serializer):
        # Allow anonymous report creation
        if self.request.user and self.request.user.is_authenticated:
            serializer.save(reported_by=self.request.user)
        else:
            serializer.save(reported_by=None)


class CameraVideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for camera videos.
    """
    queryset = CameraVideo.objects.all()
    serializer_class = CameraVideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        camera_id = self.request.query_params.get('camera_id')
        if camera_id:
            return CameraVideo.objects.filter(camera_id=camera_id)
        return CameraVideo.objects.all()


class SearchResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for search results (read-only).
    """
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        report_id = self.request.query_params.get('report_id')
        if report_id:
            return SearchResult.objects.filter(report_id=report_id).order_by('-confidence')
        return SearchResult.objects.all()
