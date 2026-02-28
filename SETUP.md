# Setup Guide - Missing Persons Alert System

## Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space

### Software Requirements
- Python 3.9+ (download from https://www.python.org/)
- Node.js 16+ (download from https://nodejs.org/)
- Git (optional, but recommended)

## Step-by-Step Setup

### Step 1: Clone or Download Project

Navigate to your desired directory and ensure you have the project files.

### Step 2: Backend Setup

#### Windows

Open Command Prompt and navigate to backend folder:

```bash
cd missing_persons_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install Django and dependencies
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 Pillow python-decouple

# Run database migrations
python manage.py migrate --noinput

# Create sample data and admin user
python manage.py populate_sample_data

# Test the setup
python manage.py check
```

#### Linux/macOS

```bash
cd missing_persons_backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 Pillow python-decouple

# Run migrations
python manage.py migrate --noinput

# Create sample data
python manage.py populate_sample_data

# Verify setup
python manage.py check
```

### Step 3: Frontend Setup

Open a new terminal and navigate to frontend folder:

```bash
cd missing_persons_frontend

# Install dependencies
npm install

# Create environment file
# On Windows:
echo REACT_APP_API_URL=http://localhost:8000/api > .env

# On Linux/Mac:
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
```

### Step 4: Start the Servers

#### Terminal 1: Backend Server

```bash
cd missing_persons_backend

# Windows
venv\Scripts\activate
python manage.py runserver

# Linux/Mac
source venv/bin/activate
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Django version 4.2.7, using settings 'config.settings'
```

#### Terminal 2: Frontend Server

```bash
cd missing_persons_frontend
npm start
```

You should see:
```
Compiled successfully!
You can now view missing_persons_frontend in the browser.
  Local:            http://localhost:3000
```

### Step 5: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api

### Step 6: Login with Default Credentials

**Admin Panel**:
- Username: `admin`
- Password: `admin123`

**App**:
- No authentication required for report filing
- Admin dashboard requires login

## File Structure After Setup

```
missing_persons/
├── missing_persons_backend/
│   ├── venv/                          # Python virtual environment
│   ├── db.sqlite3                     # Database (created after migrations)
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── apps/
│   └── ml_pipeline/
├── missing_persons_frontend/
│   ├── node_modules/                  # Node packages
│   ├── src/
│   ├── public/
│   ├── .env                          # Frontend config
│   ├── package.json
│   └── package-lock.json
└── README.md
```

## Verification Checklist

After setup, verify everything works:

- [ ] Backend server running on http://localhost:8000
- [ ] Frontend loads on http://localhost:3000
- [ ] Admin panel accessible at http://localhost:8000/admin
- [ ] Can log in with admin/admin123
- [ ] Can see 4 sample locations (Library, Canteen, Parking Lot, Gym)
- [ ] Can see cameras listed for each location
- [ ] API responds to requests

### Test the API

In a new terminal, test the API:

```bash
# Get all locations
curl http://localhost:8000/api/reports/locations/

# Get all cameras
curl http://localhost:8000/api/reports/cameras/

# Get all reports
curl http://localhost:8000/api/reports/reports/
```

## Sample Data

After running `populate_sample_data`, the system has:

**Locations**:
- Library
- Canteen  
- Parking Lot
- Gym

**Cameras**:
- Library: Entrance, Study Area, Exit
- Canteen: Main Hall, Serving Area
- Parking Lot: Entrance, Level 1, Level 2
- Gym: Entrance, Main Floor

**Users**:
- admin (admin123) - Full access

## Optional: Install ML Dependencies

For full facial recognition capability:

```bash
cd missing_persons_backend

# Activate virtual environment first
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install ML packages
pip install opencv-python==4.8.1.78 numpy scipy deepface ultralytics

# This will take 5-10 minutes depending on internet speed
```

**Note**: YOLO model file (`models/best.pt`) needs to be obtained separately.

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution**: Ensure virtual environment is activated and pip install was successful.

```bash
# Verify environment is activated (should see (venv) in terminal)
# If not:
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstall Django
pip install -r requirements.txt
```

### Issue: "Port 8000 is already in use"

**Solution**: Use a different port:

```bash
python manage.py runserver 0.0.0.0:8001
# Then change REACT_APP_API_URL in .env to http://localhost:8001/api
```

### Issue: "Port 3000 is already in use"

**Solution**: Kill the process using port 3000 or use a different port:

```bash
# Linux/Mac
sudo lsof -ti:3000 | xargs kill -9

# Windows - Open Task Manager and find Node.js process, then End Task

# Or use a different port:
PORT=3001 npm start
```

### Issue: CORS errors in browser console

**Solution**: Ensure backend is running and CORS is configured.

1. Check `.env` in backend has correct settings
2. Ensure backend is running on 8000
3. Check browser console for exact error
4. Restart frontend with `npm start`

### Issue: "Could not CREATE TABLE" database errors

**Solution**: Reset the database:

```bash
cd missing_persons_backend

# Delete the database
# Windows: del db.sqlite3
# Linux/Mac: rm db.sqlite3

# Recreate it
python manage.py migrate --noinput
python manage.py populate_sample_data
```

### Issue: Admin credentials not working

**Solution**: The populate_sample_data command creates credentials:
- Username: `admin`
- Password: `admin123`

If not working, recreate:

```bash
python manage.py createsuperuser
# Follow prompts to create new admin user
```

## Next Steps

1. **Upload Test Videos**: Add camera videos for testing search functionality
2. **Configure Locations**: Add your actual locations and camera setup
3. **Set Up Notifications**: Configure email/SMS alerts
4. **Optimize Images**: If using facial recognition, optimize YOLO model on your camera footage
5. **Deploy**: Move to production with PostgreSQL and proper server setup

## Need Help?

- Check the README.md for system overview
- Review Django documentation: https://docs.djangoproject.com/
- Review React documentation: https://react.dev/
- Check individual app documentation in comments

## Performance Tips

- Keep virtual environment activated while working
- Use `npm run build` before deployment
- Consider using a reverse proxy (nginx) in production
- Monitor disk space for video storage
- Regular database backups in production

