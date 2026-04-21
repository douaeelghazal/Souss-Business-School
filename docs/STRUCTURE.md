# Project Structure Guide

## Directory Organization

```
Busniness_School_Website-main/
│
├── backend/                      # Django Backend
│   ├── config/                  # Settings & Configuration
│   ├── data/                    # Database & Local Data
│   │   └── db.sqlite3           # Development database
│   ├── ecole/                   # Django app settings
│   ├── school/                  # Django project settings
│   ├── playground/              # Main Django app
│   │   ├── models.py            # Database models
│   │   ├── views.py             # View logic
│   │   ├── forms.py             # Django forms
│   │   ├── admin.py             # Admin interface
│   │   ├── urls.py              # URL routing
│   │   ├── templates/           # HTML templates
│   │   ├── static/              # CSS, JS, images
│   │   ├── tests.py             # Unit tests
│   │   └── migrations/          # Database migrations
│   ├── manage.py                # Django CLI
│   └── requirements.txt         # Python dependencies
│
├── frontend/                     # Frontend Assets
│   ├── assets/                  # Organized assets (future use)
│   ├── media/                   # User uploads
│   │   ├── acceuil_image/
│   │   ├── deplomes/
│   │   ├── equipe_images/
│   │   ├── events_images/
│   │   ├── formations/
│   │   ├── news_images/
│   │   └── professors/
│   └── staticfiles/             # Compiled static files (production)
│
├── scripts/                      # Management & Setup Scripts
│   ├── setup.ps1                # Initial setup script
│   └── runserver.ps1            # Start development server
│
├── docs/                         # Documentation
│   ├── STRUCTURE.md             # This file
│   ├── SETUP.md                 # Setup instructions
│   └── API.md                   # API documentation (if needed)
│
├── .venv/                        # Python virtual environment
├── .env                          # Environment variables (local)
├── .env.example                  # Environment template
├── README.md                     # Main project README
├── manage.py                     # Root symlink to backend/manage.py
└── requirements.txt              # Root symlink to backend/requirements.txt
```

## Folder Purposes

### Backend (`backend/`)
Contains all Django server-side code:
- **config/** - Settings and configuration files
- **data/** - Database and local data storage
- **playground/** - Main application with models, views, and templates
- **manage.py** - Django command-line interface

### Frontend (`frontend/`)
Contains all frontend assets:
- **media/** - User-uploaded files (diplomas, images, documents)
- **staticfiles/** - Compiled static files for production
- **assets/** - Organized assets for development

### Scripts (`scripts/`)
Helpful utility scripts:
- **setup.ps1** - Initial project setup
- **runserver.ps1** - Start development server

### Docs (`docs/`)
Project documentation:
- **STRUCTURE.md** - This file (folder organization)
- **SETUP.md** - Setup and installation guide
- **API.md** - API reference (if applicable)

## Key Files

| File | Location | Purpose |
|------|----------|---------|
| Database | `backend/data/db.sqlite3` | Development database |
| Django Settings | `backend/ecole/settings.py` | Primary Django settings |
| Requirements | `backend/requirements.txt` | Python dependencies |
| Templates | `backend/playground/templates/` | HTML templates |
| Static Files | `backend/playground/static/` | CSS, JS, images (development) |
| Media Upload | `frontend/media/` | User uploads |
| Compiled Static | `frontend/staticfiles/` | Production static files |

## Workflow

### Initial Setup
```bash
.\scripts\setup.ps1
```

### Development
```bash
.\scripts\runserver.ps1
```
Server runs on http://localhost:8000

### Deployment
```bash
cd backend
python manage.py collectstatic
```
This gathers all static files to `frontend/staticfiles/`

## Environment

- **Local Development**: Uses `backend/data/db.sqlite3` and SQLite
- **Production Ready**: Configured for PostgreSQL via `DATABASE_URL` env variable
- **Settings**: Use `.env` file for local configuration, `.env.example` as template
