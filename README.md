# Missing Persons Alert System

A comprehensive AI-powered system for detecting missing persons from CCTV footage. The system uses facial recognition to automatically search video streams and alert when matches are found.

## Architecture

```
Report Filed → Zone Selected → Cameras Chosen → AI Search → Results
```

### System Components

- **Frontend (React)**: User interface for filing reports and admin dashboard
- **Backend (Django)**: REST API for managing reports, locations, cameras, and search jobs
- **ML Pipeline (Python)**: Facial detection, embedding generation, and face matching
- **Database**: SQLite (default) or PostgreSQL (production)

## Project Structure

```
missing_persons/
├── missing_persons_backend/       # Django REST API
│   ├── apps/
│   │   ├── users/                # User management & authentication
│   │   ├── reports/              # Reports, locations, cameras
│   │   └── search/               # Search jobs & results
│   ├── ml_pipeline/              # ML pipeline wrapper
│   ├── config/                   # Django settings
│   ├── manage.py
│   └── requirements.txt
├── missing_persons_frontend/      # React application
│   ├── public/
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Main pages
│   │   ├── services/             # API client
│   │   └── styles/
│   ├── package.json
│   └── .env
├── setup_backend.bat/.sh          # Setup scripts
├── setup_frontend.bat
└── README.md
```

## Quick Start

### Backend Setup (Windows)

```bash
cd missing_persons_backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 Pillow python-decouple

# For ML features (optional, requires more setup)
# pip install opencv-python numpy scipy deepface ultralytics

# Run migrations
python manage.py migrate --noinput

# Create sample data
python manage.py populate_sample_data

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Backend Setup (Linux/Mac)

```bash
cd missing_persons_backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 Pillow python-decouple

# Run migrations & populate data
python manage.py migrate --noinput
python manage.py populate_sample_data

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

```bash
cd missing_persons_frontend

# Install dependencies
npm install

# Create environment file
echo REACT_APP_API_URL=http://localhost:8000/api > .env

# Start development server
npm start
```

The application will open at `http://localhost:3000`

## Default Credentials

After running `populate_sample_data`:
- **Username**: admin
- **Password**: admin123

## API Endpoints

### Reports API
- `GET /api/reports/reports/` - List all reports
- `POST /api/reports/reports/` - Create new report
- `GET /api/reports/reports/{id}/` - Get report details
- `GET /api/reports/reports/{id}/search_results/` - Get search results for a report

### Locations API
- `GET /api/reports/locations/` - List all locations
- `POST /api/reports/locations/` - Create location

### Cameras API
- `GET /api/reports/cameras/` - List all cameras
- `GET /api/reports/cameras/?location_id=1` - Get cameras by location

### Search API
- `POST /api/search/jobs/start_search/` - Start a search job
  ```json
  {
    "report_id": 1,
    "camera_ids": [1, 2, 3]
  }
  ```
- `GET /api/search/jobs/` - List all search jobs
- `GET /api/search/jobs/{id}/` - Get job details

## System Flow

### 1. File Missing Person Report
- User visits frontend homepage
- Uploads missing person photo
- Selects last seen location
- Enters description
- Submits report

### 2. Admin Views Report
- Admin login to dashboard
- Sees new report notification
- Location highlighted on map

### 3. Select Zone & Cameras
- Admin clicks location on map
- System shows all cameras in that zone
- Admin selects specific cameras
- Clicks "Start Search"

### 4. AI Processing
- System fetches videos from selected cameras
- Generates embedding from missing person photo
- For each video:
  - Extracts keyframes
  - Detects faces (YOLO)
  - Generates embeddings (FaceNet)
  - Compares with missing person embedding
  - Saves matches if confidence > threshold

### 5. Results & Alert
- Matches found are saved with:
  - Camera name
  - Timestamp
  - Face snapshot
  - Confidence score
- If high confidence: Alert sent to admin
- Results displayed in dashboard

## Features

### Current (MVP)
- ✅ Report filing with photo upload
- ✅ Location management with map interface
- ✅ Camera management per location
- ✅ Search job processing
- ✅ Facial detection with YOLO
- ✅ Face embedding generation with FaceNet
- ✅ Confidence-based matching
- ✅ Admin dashboard
- ✅ API documentation

### Future Enhancements
- Photo angle generation (AI synthesis)
- GFPGAN for CCTV image enhancement
- ArcFace model for better accuracy
- Multi-photo upload with ensemble matching
- Face restoration preprocessing
- Celery for async job processing
- PostgreSQL for production
- Police API integration
- Message queue for notifications
- Pre-indexed video database
- Performance optimization
- Advanced search filters

## Database Schema

### Users
- Custom User model with roles: admin, operator, reporter
- Token authentication support

### Reports
- Missing person name
- Photo (uploaded)
- Description
- Last seen location & time
- Status: filed, searching, found, closed

### Locations
- Name
- GPS coordinates (latitude, longitude)
- Multiple cameras per location

### Cameras
- Name
- Location reference
- Status (active/inactive)

### CameraVideos
- Camera reference
- Video file
- Recording timestamp
- Duration

### SearchResults
- Report reference
- Camera reference
- Match timestamp
- Confidence score (0-1)
- Confidence level: high (>90%), medium (70-90%), low (<70%)
- Face snapshot
- Embedding vector

### SearchJobs
- Report reference
- Selected cameras
- Status: pending, processing, completed, failed
- Progress tracking
- Matches count

## Environment Variables

Create `.env` file in backend directory:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Performance Considerations

### For Review
- Using SQLite (sufficient for demo)
- Single-threaded processing (sufficient for demo)
- Basic confidence threshold (0.4)

### For Production
- Switch to PostgreSQL
- Use Celery for async processing
- Implement connection pooling
- Add caching layer
- Optimize video processing
- Use Redis for job queue
- Deploy with Gunicorn/uWSGI
- Use nginx as reverse proxy

## Troubleshooting

### ImportError: No module named 'cv2'
ML features require opencv-python. Install with:
```bash
pip install opencv-python numpy scipy deepface ultralytics
```

### Database errors
Reset database and migrations:
```bash
rm db.sqlite3
python manage.py migrate --noinput
python manage.py populate_sample_data
```

### CORS errors
Check CORS_ALLOWED_ORIGINS in settings.py and .env file

### Port already in use
Change port:
```bash
python manage.py runserver 0.0.0.0:8001
```

## Technologies Used

### Backend
- Django 4.2
- Django REST Framework 3.14
- Pillow (image handling)
- python-decouple (config management)
- OpenCV (image processing)
- FaceNet/DeepFace (embedding generation)
- YOLO (face detection)

### Frontend
- React 18
- React Router 6
- Axios (HTTP client)
- Leaflet (maps)
- react-leaflet (React wrapper)
- react-dropzone (file upload)

### Database
- SQLite (dev)
- PostgreSQL (production ready)

### DevOps
- Virtual Environment (Python)
- npm (Node packages)

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

[Add your license here]

## Support

For issues or questions, contact: [support@example.com]

## Next Steps

1. Install ML packages: `pip install opencv-python deepface ultralytics`
2. Upload sample videos to test search functionality
3. Fine-tune YOLO model on your camera footage
4. Deploy to production environment
5. Integrate with police database
6. Add SMS/Email notifications
7. Performance optimization based on real data

