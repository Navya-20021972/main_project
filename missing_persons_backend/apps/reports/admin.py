from django.contrib import admin
from .models import Location, Camera, Report, CameraVideo, SearchResult

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'created_at']
    search_fields = ['name']

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active', 'created_at']
    list_filter = ['location', 'is_active']
    search_fields = ['name', 'location__name']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['missing_person_name', 'status', 'last_seen_location', 'created_at']
    list_filter = ['status', 'last_seen_location', 'created_at']
    search_fields = ['missing_person_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CameraVideo)
class CameraVideoAdmin(admin.ModelAdmin):
    list_display = ['camera', 'recording_date', 'duration', 'is_processed']
    list_filter = ['camera', 'is_processed', 'recording_date']

@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['report', 'camera', 'confidence', 'match_time']
    list_filter = ['confidence_level', 'created_at']
    search_fields = ['report__missing_person_name']
    readonly_fields = ['created_at']
