# Setup Guide

## Quick Start

### 1. Run Setup Script (Recommended)
```bash
.\scripts\setup.ps1
```

This automatically:
- Creates a virtual environment
- Installs dependencies
- Runs database migrations
- Creates a superuser account

### 2. Manual Setup

#### Prerequisites
- Python 3.8+
- pip or poetry
- Git

#### Step-by-Step

**1. Create Virtual Environment**
```bash
python -m venv .venv
```

**2. Activate Virtual Environment**

Windows (PowerShell):
```bash
.\.venv\Scripts\Activate.ps1
```

Windows (Command Prompt):
```bash
.venv\Scripts\activate.bat
```

Linux/Mac:
```bash
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**4. Create Database**
```bash
python manage.py migrate
```

**5. Create Admin User**
```bash
python manage.py createsuperuser
```

**6. Start Development Server**
```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

## Environment Configuration

### Create .env File

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Key Settings:**
- `DEBUG=True` - Enable debug mode (development only)
- `SECRET_KEY` - Django secret key (generate a new one for production)
- `ALLOWED_HOSTS` - Allowed hostnames
- `DATABASE_URL` - PostgreSQL URL for production
- `EMAIL_HOST_USER` - Email configuration for notifications
- `EMAIL_HOST_PASSWORD` - Email password

## Running the Application

### Development Server

From the root directory after activating venv:

```bash
cd backend
python manage.py runserver
```

Or use the convenience script:

```bash
.\scripts\runserver.ps1
```

### Admin Panel

Access the Django admin at:
```
http://localhost:8000/admin/
```

Use the superuser credentials created during setup.

## Static Files & Media

### Development
Static files are served automatically from:
- `backend/playground/static/` - CSS, JS, images

### Production
Collect static files:
```bash
cd backend
python manage.py collectstatic
```

Files are gathered to `frontend/staticfiles/`

## Database

### SQLite (Development)
- Location: `backend/data/db.sqlite3`
- Automatically created on first migration

### PostgreSQL (Production)
Set `DATABASE_URL` environment variable:
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Troubleshooting

### Virtual Environment Not Activating
```bash
# Bypass execution policy (Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### Port 8000 Already in Use
```bash
# Use a different port
python manage.py runserver 8001
```

### Database Migration Issues
```bash
# Reset database (WARNING: Deletes all data)
rm backend/data/db.sqlite3
python manage.py migrate
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Next Steps

1. Review [STRUCTURE.md](STRUCTURE.md) for project organization
2. Check the admin panel at `/admin/`
3. Explore templates in `backend/playground/templates/`
4. Review [API.md](API.md) for API endpoints (if applicable)
