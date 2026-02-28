from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reports'

router = DefaultRouter()
router.register(r'locations', views.LocationViewSet, basename='location')
router.register(r'cameras', views.CameraViewSet, basename='camera')
router.register(r'reports', views.ReportViewSet, basename='report')
router.register(r'videos', views.CameraVideoViewSet, basename='video')
router.register(r'results', views.SearchResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]
