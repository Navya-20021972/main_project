from django.contrib import admin
from .models import SearchJob

@admin.register(SearchJob)
class SearchJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'report', 'status', 'progress', 'matches_found', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['report__missing_person_name']
    readonly_fields = ['created_at', 'started_at', 'completed_at']
