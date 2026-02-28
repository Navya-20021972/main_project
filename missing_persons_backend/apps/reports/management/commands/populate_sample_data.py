from django.core.management.base import BaseCommand
from apps.reports.models import Location, Camera
from apps.users.models import User
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create sample locations
        locations_data = [
            {
                'name': 'Library',
                'description': 'Central Library Building',
                'latitude': 40.7128,
                'longitude': -74.0060
            },
            {
                'name': 'Canteen',
                'description': 'Main Cafeteria',
                'latitude': 40.7131,
                'longitude': -74.0055
            },
            {
                'name': 'Parking Lot',
                'description': 'Main Parking Area',
                'latitude': 40.7125,
                'longitude': -74.0065
            },
            {
                'name': 'Gym',
                'description': 'Sports Complex',
                'latitude': 40.7135,
                'longitude': -74.0050
            }
        ]

        locations = {}
        for loc_data in locations_data:
            loc, created = Location.objects.get_or_create(
                name=loc_data['name'],
                defaults={
                    'description': loc_data['description'],
                    'latitude': loc_data['latitude'],
                    'longitude': loc_data['longitude']
                }
            )
            locations[loc_data['name']] = loc
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created location: {loc.name}'))

        # Create sample cameras
        camera_data = {
            'Library': ['Entrance', 'Study Area', 'Exit'],
            'Canteen': ['Main Hall', 'Serving Area'],
            'Parking Lot': ['Entrance', 'Level 1', 'Level 2'],
            'Gym': ['Entrance', 'Main Floor']
        }

        for location_name, cameras in camera_data.items():
            location = locations[location_name]
            for camera_name in cameras:
                camera, created = Camera.objects.get_or_create(
                    name=camera_name,
                    location=location,
                    defaults={
                        'description': f'{camera_name} camera in {location_name}',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created camera: {camera.name}'))

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.WARNING('Default admin credentials:'))
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
