# Deployment Instructions for PythonAnywhere

## Prerequisites
- Python 3.8 or higher
- PostgreSQL database (if using PythonAnywhere's database)

## Steps to Deploy on PythonAnywhere

### 1. Create a New Web App
1. Log in to PythonAnywhere
2. Go to the "Web" tab
3. Click "Add a new web app"
4. Choose "Manual configuration"
5. Select Python 3.8 or higher

### 2. Configure the Web App
1. In the "Code" section, set the path to your project
2. Set the virtual environment path
3. In the "WSGI configuration file", update the path to your project

### 3. Set Up Database
1. Create a PostgreSQL database in PythonAnywhere
2. Update the database settings in `Gymnastic/settings.py` with your database credentials

### 4. Install Dependencies
1. Activate your virtual environment
2. Run: `pip install -r requirements.txt`

### 5. Collect Static Files
1. Run: `python manage.py collectstatic`
2. Answer "yes" to collect static files

### 6. Run Migrations
1. Run: `python manage.py migrate`

### 7. Restart the Web App
1. Go to the "Web" tab
2. Click "Reload" to restart your web app

## Environment Variables
Make sure to set the following environment variables:
- `PYTHONANYWHERE=1` (to indicate PythonAnywhere deployment)
- Your database credentials