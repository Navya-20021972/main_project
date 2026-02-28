from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Location.objects.all().order_by('name')


class CameraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cameras to be viewed or edited.
    """
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]
    
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
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReportDetailSerializer
        return ReportSerializer
    
    def get_queryset(self):
        # Users can see their own reports, admins see all
        user = self.request.user
        if user.role == 'admin':
            return Report.objects.all()
        return Report.objects.filter(reported_by=user)
    
    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def search_results(self, request, pk=None):
        """Get search results for a specific report"""
        report = self.get_object()
        results = SearchResult.objects.filter(report=report).order_by('-confidence')
        serializer = SearchResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_report(self, request):
        """Create a new report"""
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reported_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
