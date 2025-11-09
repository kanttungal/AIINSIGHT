# Deploying AI-Insight on Render

## Prerequisites
- Python 3.13 installed
- Required packages listed in `requirements.txt`

## Steps

1. **Install Dependencies**
   Run the following command to install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database**
   Ensure your `ai_blog/settings.py` is configured for the database (e.g., PostgreSQL).

3. **Start the Application**
   Use Gunicorn to start the application:
   ```bash
   gunicorn ai_blog.wsgi:application
   ```

4. **Deploy with Render**
   - Update `render.yaml` with the correct build and start commands as shown.
   - Commit changes and push to Render for deployment.

5. **Troubleshooting**
   - If Pillow installation fails, try:
     ```bash
     pip install --no-binary Pillow -r requirements.txt
     ```
   - Ensure `setuptools` and `wheel` are up to date:
     ```bash
     pip install --upgrade setuptools wheel
