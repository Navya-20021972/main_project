from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from apps.reports.models import Location, Camera, CameraVideo
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Load pre-recorded videos from media folder into database'

    def handle(self, *args, **options):
        # Base path for videos
        base_video_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'media' / 'videos'

        # Zone and video configuration
        zones = {
            'department': {
                'location_name': 'Department',
                'videos': ['vid1.mp4', 'vid2.mp4', 'vid3.mp4']
            },
            'canteen': {
                'location_name': 'Canteen',
                'videos': ['vid1.mp4', 'vid2.mp4']
            },
            'library': {
                'location_name': 'Library',
                'videos': []
            }
        }

        # Create/update cameras and load videos for each zone
        for zone_folder, config in zones.items():
            location_name = config['location_name']
            video_files = config['videos']

            # Get or create location
            location, created = Location.objects.get_or_create(
                name=location_name,
                defaults={
                    'description': f'{location_name} Zone',
                    'latitude': 40.7128 + (hash(location_name) % 100) / 1000,
                    'longitude': -74.0060 + (hash(location_name) % 100) / 1000
                }
            )
            self.stdout.write(f"Location: {location.name} {'(created)' if created else '(exists)'}")

            # Create 3 cameras for this zone
            for cam_idx in range(1, 4):
                camera, cam_created = Camera.objects.get_or_create(
                    name=f'{location_name}_Camera_{cam_idx}',
                    location=location,
                    defaults={
                        'description': f'Camera {cam_idx} in {location_name}',
                        'is_active': True
                    }
                )
                self.stdout.write(f"  Camera: {camera.name} {'(created)' if cam_created else '(exists)'}")

                # Load video for this camera if available
                if cam_idx <= len(video_files):
                    video_file = video_files[cam_idx - 1]
                    video_path = base_video_path / zone_folder / video_file

                    if video_path.exists():
                        # Check if video already loaded
                        existing_video = CameraVideo.objects.filter(
                            camera=camera,
                            video_file__icontains=video_file
                        ).first()

                        if existing_video:
                            self.stdout.write(f"    Video: {video_file} (already loaded)")
                        else:
                            # Load video into database
                            with open(video_path, 'rb') as f:
                                video_data = ContentFile(f.read(), name=video_file)
                                
                                camera_video = CameraVideo.objects.create(
                                    camera=camera,
                                    video_file=video_data,
                                    recording_date=timezone.now(),
                                    duration=0  # Set to 0 or calculate from actual video duration
                                )
                                self.stdout.write(f"    ✓ Video loaded: {video_file}")
                    else:
                        self.stdout.write(f"    ✗ Video file not found: {video_path}")
                else:
                    self.stdout.write(f"    (No video for this camera)")

        self.stdout.write(self.style.SUCCESS('\n✅ Video import completed!'))
