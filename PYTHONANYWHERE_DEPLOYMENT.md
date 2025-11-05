# Render Deployment Guide

This guide explains how to deploy the AI Blog Django application to Render.

## Prerequisites

1. A PythonAnywhere account (free or paid tier)
2. Your project code uploaded to PythonAnywhere (via Git or direct upload)

## Deployment Steps

### 1. Upload Your Code

You have two options to get your code to PythonAnywhere:

**Option A: Using Git (Recommended)**
```bash
# Clone your repository
git clone https://github.com/kanttungal/AIINSIGHT.git
cd AIINSIGHT
```

**Option B: Direct Upload**
- Use the PythonAnywhere "Upload a file" option in the Files tab
- Upload your project files to a directory like `/home/yourusername/ai-blog/`

### 2. Set Up Your Virtual Environment

Open a Bash console in PythonAnywhere and run:

```bash
# Navigate to your project directory
cd /home/kanttungal/ai-blog

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Your Django Settings

The project includes a PythonAnywhere-specific settings file (`ai_blog/settings_pythonanywhere.py`) that:
- Configures the database for SQLite (default)
- Sets appropriate static and media file paths
- Configures allowed hosts for PythonAnywhere
- Sets security settings for production

### 4. Run Initial Setup

While still in your virtual environment:

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser
```

### 5. Configure the Web App

1. Go to the "Web" tab in your PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" (not the Django autoconfig)
4. Select Python 3.x version

### 6. Configure Render Settings

In the Render dashboard, ensure the following settings are configured:

**Project Directory:**
```
/home/kanttungal/AI_Blogs
```

**Build Command:**
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

**Start Command:**
```bash
gunicorn ai_blog.wsgi:application
```

**Environment Variables:**
- `DATABASE_URL`: Your Render PostgreSQL database URL
- `SECRET_KEY`: Your Django secret key
- `ALLOWED_HOSTS`: Your Render app domain (e.g., `your-app-name.onrender.com`)

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/kanttungal/ai-blog'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to point to your settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'ai_blog.settings_pythonanywhere'

# Activate your virtual env
activate_this = '/home/kanttungal/ai-blog/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django
import django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7. Configure Static Files

In the "Static files" section, add:

- URL: `/static/`
- Path: `/home/yourusername/ai-blog/staticfiles`

### 8. Configure Media Files (if needed)

If your application serves media files:

- URL: `/media/`
- Path: `/home/yourusername/ai-blog/media`

### 9. Set Environment Variables

In the "Environment variables" section, add:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
DOMAIN_NAME=your-username.pythonanywhere.com
```

### 10. Deploy via Render Dashboard

1. Go to the [Render Dashboard](https://dashboard.render.com)
2. Create a new Web Service
3. Select "Django" as the framework
4. Set the project directory to `/home/kanttungal/AI_Blogs`
5. Use the `render.yaml` file in your repository for configuration
6. Set environment variables in the "Variables" tab
7. Click "Launch" to deploy

## Database Considerations

The application is configured to use SQLite by default, which works well for PythonAnywhere. If you want to use MySQL (available on paid accounts):

1. Create a MySQL database in the PythonAnywhere dashboard
2. Update `ai_blog/settings_pythonanywhere.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourusername$default',
        'USER': 'yourusername',
        'PASSWORD': 'your-database-password',
        'HOST': 'yourusername.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure your project path is correctly added to sys.path in the WSGI file
2. **Static files not loading**: Check that the static files mapping is correct in the web app configuration
3. **Permission errors**: Ensure your files have the correct permissions (755 for directories, 644 for files)

### Checking Logs

1. Check the error log in the Web tab for application errors
2. Check the server log for web server issues

### Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Check Django settings
python manage.py diffsettings

# Check for missing migrations
python manage.py showmigrations

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
```

## Updating Your Application

To update your application after making changes:

1. Upload your new code (or git pull if using Git)
2. If you've changed dependencies: `pip install -r requirements.txt`
3. If you've added new static files: `python manage.py collectstatic --noinput`
4. If you've added new migrations: `python manage.py migrate`
5. Reload your web app in the PythonAnywhere dashboard

## Additional Notes

- PythonAnywhere has a whitelist of allowed outgoing IP addresses for free accounts
- Free accounts have limited CPU time and bandwidth
- Consider upgrading to a paid account for production applications
- Regularly back up your database and files
