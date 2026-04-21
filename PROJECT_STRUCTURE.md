# Project Structure

This project has been reorganized into a clear **Backend** and **Frontend** separation.

## Directory Layout

```
Busniness_School_Website-main/
├── backend/                    # Django backend code
│   ├── ecole/                 # Django settings module
│   │   └── settings.py        # Main Django configuration
│   ├── school/                # Django project settings
│   │   ├── settings.py        # Alternative settings
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── playground/            # Main Django application
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── templates/         # HTML templates
│   │   ├── static/            # CSS, JavaScript, images
│   │   └── migrations/        # Database migrations
│   └── manage.py              # Django management command
│
├── frontend/                   # Frontend assets
│   ├── media/                 # User-uploaded media files
│   │   ├── acceuil_image/
│   │   ├── deplomes/
│   │   ├── equipe_images/
│   │   ├── events_images/
│   │   ├── formations/
│   │   ├── news_images/
│   │   └── professors/
│   └── staticfiles/           # Compiled static files (production)
│
├── .venv/                     # Python virtual environment
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # Development database
├── manage.py                  # Root manage.py (symlink to backend/manage.py)
├── README.md                  # Project README
└── ...other config files
```

## Running the Application

### Development Server

To run the development server from the root directory:

```bash
cd backend
python manage.py runserver
```

Or directly from the root if you have a manage.py symlink:

```bash
python manage.py runserver
```

### Collecting Static Files

To collect all static files to the frontend/staticfiles directory:

```bash
cd backend
python manage.py collectstatic
```

This will gather all static files from `playground/static/` and place them in `frontend/staticfiles/`.

## Static Files & Media

### Static Files
- **Source**: `backend/playground/static/` - Development static files (CSS, JS, images)
- **Destination**: `frontend/staticfiles/` - Production static files (collected via `collectstatic`)
- **Served from**: `/static/` URL

### Media Files
- **Location**: `frontend/media/` - User-uploaded files
- **Served from**: `/media/` URL

## Django Settings

The main Django configuration files have been updated to reference the new paths:

- `backend/school/settings.py` - Primary settings (uses ecole settings as default)
- `backend/ecole/settings.py` - Alternative settings module

Both settings files are configured to:
- Serve templates from `backend/playground/templates/`
- Collect static files to `frontend/staticfiles/`
- Store media files in `frontend/media/`

## Installation & Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   cd backend
   python manage.py migrate
   ```

4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```

5. Start development server:
   ```bash
   python manage.py runserver
   ```

## Benefits of This Structure

- **Clear Separation**: Backend (Python/Django) and Frontend (Static Assets) are isolated
- **Production Ready**: Easy to serve static files separately in production
- **Scalability**: Frontend assets can be served from a CDN or separate server
- **Maintenance**: Easier to understand and modify each part independently
- **Deployment**: Cleaner deployment process with separated concerns
