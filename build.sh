#!/usr/bin/env bash
# exit on error
set -o errexit

# Python version check
echo "Python version: $(python --version)"

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install additional production dependencies
echo "Installing production dependencies..."
pip install gunicorn dj-database-url psycopg2-binary

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity=2

# Run migrations
echo "Running migrations..."
python manage.py migrate --verbosity=2

# Create superuser if it doesn't exist (optional)
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin');
    print('Superuser created');
else:
    print('Superuser already exists');
"

echo "Build completed successfully!"
