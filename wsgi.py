# This file is used by PythonAnywhere to deploy the Django application
# It should be configured in the PythonAnywhere web app configuration

import os
import sys

# Add your project directory to the sys.path
# Replace 'yourusername' and 'yourproject' with your actual PythonAnywhere username and project directory
project_home = '/home/kanttungal/AI_Blogs/AI_Blogs'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to point to your settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'AI_Blogs.ai_blog.settings_production'

activate_this = os.path.expanduser('~/venv/bin/activate_this.py')
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django
import django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
