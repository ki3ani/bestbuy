#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

# Create superuser if not already exists
echo "Creating superuser..."
python manage.py create_superuser

#Run tests
echo "Running tests..."
python manage.py test

# Start Gunicorn
echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 cleanstore.wsgi:application
