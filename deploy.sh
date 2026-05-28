#!/bin/bash

# Deployment script for PythonAnywhere

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Collect static files
python Gymnastic/manage.py collectstatic --noinput

# Run migrations
python Gymnastic/manage.py migrate

echo "Deployment completed successfully!"