from django.db import models

class SearchJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    report = models.ForeignKey('reports.Report', on_delete=models.CASCADE, related_name='search_jobs')
    cameras = models.ManyToManyField('reports.Camera', related_name='search_jobs')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    
    matches_found = models.IntegerField(default=0)
    videos_processed = models.IntegerField(default=0)
    total_videos = models.IntegerField(default=0)
    
    error_message = models.TextField(blank=True)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Search Job #{self.id} - {self.report.missing_person_name}"
    
    class Meta:
        ordering = ['-created_at']
