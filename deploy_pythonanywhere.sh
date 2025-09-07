#!/bin/bash
# Deployment script for PythonAnywhere

# Exit on error
set -e

echo "Starting PythonAnywhere deployment process..."

# Check if we're on PythonAnywhere by checking for a known directory
if [ ! -d "/home" ]; then
    echo "This script is intended to be run on PythonAnywhere."
    echo "Please run this script on your PythonAnywhere account."
    exit 1
fi

# Update the project (if using git)
if command -v git &> /dev/null; then
    echo "Updating code from repository..."
    git pull origin main
else
    echo "Git not found. Skipping code update."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

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

echo "Deployment completed successfully!"
echo ""
echo "Next steps:"
echo "1. Configure your PythonAnywhere web app to use pythonanywhere_wsgi.py"
echo "2. Set the static files mapping in PythonAnywhere:"
echo "   URL: /static/"
echo "   Path: /home/yourusername/yourproject/staticfiles"
echo "3. Reload your web app in the PythonAnywhere dashboard"
