#!/usr/bin/env python
"""
Database setup script for PythonAnywhere deployment
"""

import os
import django
from django.conf import settings

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
os.sys.path.insert(0, project_dir)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gymnastic.settings')

# Setup Django
django.setup()

print("Django setup complete for PythonAnywhere deployment")
print("Run 'python manage.py migrate' to apply database migrations")
print("Run 'python manage.py collectstatic' to collect static files")