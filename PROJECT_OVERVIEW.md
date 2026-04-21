# Project Overview

The **Souss Business School Website** is a comprehensive Django-based platform for school information management.

## Quick Navigation

- **Setup Instructions**: See [docs/SETUP.md](docs/SETUP.md)
- **Project Structure**: See [docs/STRUCTURE.md](docs/STRUCTURE.md)
- **Quick Start**: Run `.\scripts\setup.ps1`

## Project Organization

```
backend/                  Django backend & database
frontend/                 Frontend assets & media
scripts/                  Utility scripts
docs/                     Project documentation
```

### Backend Structure
- `backend/ecole/` - Django settings
- `backend/school/` - Alternative Django config
- `backend/playground/` - Main application
- `backend/data/` - Database storage
- `backend/requirements.txt` - Dependencies

### Frontend Structure
- `frontend/media/` - User uploads (images, documents)
- `frontend/staticfiles/` - Production static files
- `frontend/assets/` - Organized assets

## Key Features

✅ Responsive design for mobile/tablet/desktop  
✅ Dynamic content management (news, events, formations)  
✅ Secure admin dashboard  
✅ Team & professor directories  
✅ Alumni tracking system  
✅ Media management  
✅ Search & filtering  
✅ Production-ready security  

## Quick Start

### 1. First Time Setup
```bash
.\scripts\setup.ps1
```

### 2. Start Development Server
```bash
.\scripts\runserver.ps1
```

### 3. Access Application
- Frontend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin/

## Development

### After Initial Setup

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Navigate to backend
cd backend

# Run development server
python manage.py runserver
```

### Common Commands

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key variables:
- `DEBUG=True` - Enable debug mode (development only)
- `SECRET_KEY` - Secret key for Django
- `DATABASE_URL` - Database connection (PostgreSQL for production)
- `ALLOWED_HOSTS` - Allowed hostnames
- `EMAIL_*` - Email configuration

## Database

### Development
SQLite database located at: `backend/data/db.sqlite3`

### Production
Configure PostgreSQL via `DATABASE_URL` environment variable

## Static Files & Media

### Development
Static files served from: `backend/playground/static/`

### Production
Collect static files:
```bash
cd backend
python manage.py collectstatic
```

Collected to: `frontend/staticfiles/`

User uploads stored in: `frontend/media/`

## Project Structure

For detailed information about the project structure, see [docs/STRUCTURE.md](docs/STRUCTURE.md)

## Documentation

- **[SETUP.md](docs/SETUP.md)** - Detailed setup and installation guide
- **[STRUCTURE.md](docs/STRUCTURE.md)** - Project folder organization and purposes
- **Original [README.md](README.md)** - Full project documentation

## Troubleshooting

### Virtual Environment Issues
```bash
# Bypass execution policy (Windows PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
Remove-Item backend/data/db.sqlite3
python manage.py migrate
```

For more help, see [docs/SETUP.md](docs/SETUP.md#troubleshooting)

## Technology Stack

- **Backend**: Django 5.1+
- **Database**: SQLite (dev), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Static Files**: WhiteNoise for efficient serving
- **Security**: Django built-in + hardened configuration

## License

See [LICENSE](LICENSE) file

---

**Last Updated**: April 2026  
**Status**: Production Ready ✅
