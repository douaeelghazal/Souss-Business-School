# Souss Massa Business School Website

## Project Overview

This project is a comprehensive, production-ready website built with Django that showcases the Souss Massa Business School. The platform provides detailed information about the school's academic programs, news, events, team members, and mission, serving prospective students, current faculty, alumni, and business partners.

The website features a secure admin dashboard allowing authorized users to manage all dynamic content including news, events, formations, team members, and other resources without requiring code modifications. This ensures smooth, efficient content management for non-technical administrators.

The application has been significantly improved with enterprise-grade security, performance optimizations, and modern code quality standards suitable for production deployment.

---

## Key Features

### Content Management
- Comprehensive informational pages about school history, vision, and values
- Dynamic news and events management system with theme filtering
- Academic formations database with detailed program information
- Team and professor directories with search functionality
- Alumni network and graduate tracking system
- Multiple media integration for images, documents, and files

### User Experience
- Responsive design optimized for desktops, tablets, and mobile devices
- Case-insensitive search across programs, news, and events
- Pagination for improved performance on large datasets
- Theme-based filtering and categorization
- Accessible, user-friendly interface design
- Interactive JavaScript components for enhanced navigation

### Administrative Features
- Secure authentication system with user registration and login
- Role-based access control for administrators
- User-friendly admin dashboard for content management
- CRUD operations for all content types without code changes
- Search and filter capabilities across all entities
- Media upload and file management
- Content publishing controls (publish/unpublish functionality)

### Security and Performance
- Hardened security configuration suitable for production deployment
- Environment-based configuration management
- Comprehensive error handling and logging
- Database query optimization with pagination
- Static file compression and efficient caching
- Protection against common security vulnerabilities
- HTTPS and SSL/TLS support ready
- Database credentials and secrets protected via environment variables

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | Django | 5.1.4 |
| Programming Language | Python | 3.8+ |
| Frontend | HTML5, CSS3, JavaScript | Latest |
| Database | SQLite (default) / PostgreSQL | Configurable |
| Web Server | Gunicorn | 23.0.0 |
| Image Processing | Pillow | 11.0.0 |
| Static Files | WhiteNoise | 6.6.0 |
| API Framework | Django REST Framework | 3.14.0 |
| Configuration | python-dotenv | 1.0.0 |
| Utilities | dj-database-url, django-cors-headers, django-filter | Latest |

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
cd c:\Users\Douae\Downloads\Busniness_School_Website-main
```

### Step 2: Create and Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
copy .env.example .env
```

Edit the .env file with your configuration:
```
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 5: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser Account
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Access the website at http://127.0.0.1:8000/

---

## Project Structure

```
Busniness_School_Website/
├── school/                      # Main Django project settings
│   ├── settings.py             # Configuration (security, database, apps)
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── playground/                  # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View logic with pagination and optimization
│   ├── urls.py                 # App URL patterns
│   ├── forms.py                # Form definitions
│   ├── admin.py                # Admin interface configuration
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS, JavaScript, images
│   └── migrations/             # Database migrations
├── media/                       # User-uploaded files
├── staticfiles/                 # Collected static files (production)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── README.md                    # This file
├── IMPROVEMENTS.md              # Detailed improvement documentation
└── QUICKSTART.md               # Quick start guide

```

---

## Database Models

### Content Models
- News: Articles with themes, dates, and publication status
- Event: Events with start/end dates and theme categorization
- Formati: Academic formations with curriculum details
- Equipe: Team members with positions and biographies
- Prof: Professors with specializations

### Supporting Models
- Objec: Formation objectives and learning outcomes
- Prerequi: Prerequisites for programs
- Retour: Alumni feedback and testimonials
- Histoire: Alumni stories and case studies
- Deplome: Graduate profiles and employment information
- Alumni: Alumni network statistics and data
- Reseau: Alumni network connections
- Partner organizations and other supporting entities

---

## Security Features

### Implemented
- Secret key and sensitive credentials stored in environment variables
- Debug mode disabled by default in production
- ALLOWED_HOSTS properly configured
- User authentication required for administrative actions
- CSRF protection enabled
- SQL injection prevention through ORM
- Static files served securely with WhiteNoise
- Comprehensive error handling without information leakage

### Production-Ready Configuration
- HTTPS/SSL support with configuration ready
- Session cookie security settings
- Security headers (HSTS, X-Frame-Options, Content-Security-Policy)
- Database connection security
- Email credential protection
- Prepared for cloud deployment

---

## Performance Optimizations

### Database Efficiency
- Pagination implemented (10 items per page by default)
- Query optimization with select_related() and prefetch_related()
- N+1 query problem eliminated
- Indexed searches for better performance
- Database connection pooling ready

### Frontend Performance
- Static file compression with WhiteNoise
- CSS and JavaScript bundling support
- Image optimization capability
- Caching headers configured
- Lazy loading ready for implementation

### Search and Filtering
- Case-insensitive search with icontains
- Multi-field search capabilities (title, content, etc.)
- Theme-based filtering for news and events
- Efficient query filters

---

## Configuration Management

All sensitive configuration is managed through environment variables in the .env file:

- SECRET_KEY: Django secret key for cryptographic operations
- DEBUG: Development/production mode toggle
- ALLOWED_HOSTS: Allowed domain names
- DATABASE_URL: Database connection string
- EMAIL_HOST_USER: Email service username
- EMAIL_HOST_PASSWORD: Email service password
- SECURE_SSL_REDIRECT: HTTPS enforcement
- SESSION_COOKIE_SECURE: Secure cookie transmission
- SECURE_HSTS_SECONDS: HTTP Strict Transport Security

See .env.example for complete list of available options.

---

## Logging and Error Handling

The application includes comprehensive logging throughout all views:
- Automatic error logging for debugging
- Exception handling with graceful degradation
- Detailed error messages in development mode
- Production-safe error responses
- Database connection error handling
- File upload error management

---

## Admin Dashboard

Access the admin dashboard at /admin/ after logging in with superuser credentials.

### Available Operations
- Create, read, update, delete news articles
- Manage events and calendar
- Update formation information
- Manage team members and professors
- Maintain alumni database
- Update news themes and categories
- Manage user accounts and permissions
- Review published content

All operations can be performed without writing code.

---

## API Endpoints Ready

The following API endpoints are ready for future development (REST Framework installed):

- /api/news/ - News list and detail
- /api/events/ - Events list and detail
- /api/formations/ - Formations list and detail
- /api/team/ - Team members list
- /api/professors/ - Professors list
- Additional endpoints can be added as needed

---

## Deployment

### Local Development
```bash
python manage.py runserver
```

### Production with Gunicorn
```bash
gunicorn school.wsgi:application --bind 0.0.0.0:8000
```

### Environment Setup for Production
1. Update .env with production values
2. Set DEBUG=False
3. Generate new SECRET_KEY
4. Configure database (PostgreSQL recommended)
5. Set SECURE_SSL_REDIRECT=True
6. Configure domain in ALLOWED_HOSTS
7. Set up email service credentials
8. Use reverse proxy (Nginx recommended)
9. Enable HTTPS with SSL certificate

### Cloud Platform Deployment
The project includes Procfile for Heroku and Render.com deployment. Modify environment variables in the platform's configuration panel.

---

## Testing

To test the improvements:

### Test Pagination
Navigate to any list view (e.g., /news_list/) and verify pagination controls appear.

### Test Search
Try searching with different cases (e.g., "FORMATION" vs "formation") to verify case-insensitive search.

### Test Error Handling
Monitor logs for proper error messages in case of exceptions.

### Test Performance
Use browser DevTools to verify reduced number of database requests.

---

## Troubleshooting

### Module Import Errors
Ensure all packages are installed: `pip install -r requirements.txt`

### Environment Variables Not Loading
- Verify .env file exists in project root
- Ensure python-dotenv is installed
- Restart development server after creating .env

### Email Not Sending
- Configure valid email credentials in .env
- Set EMAIL_BACKEND to smtp
- Verify EMAIL_HOST, EMAIL_PORT settings
- For Gmail, use app-specific password

### Database Errors
- Ensure database file has write permissions
- Run migrations: `python manage.py migrate`
- Check DATABASE_URL format in .env

### Static Files Not Loading
- Run collectstatic: `python manage.py collectstatic`
- Verify STATIC_URL and STATIC_ROOT settings
- Check static files permissions

---

## Contributing Guidelines

When contributing to this project:

1. Ensure all new features include error handling
2. Add logging for debugging capability
3. Optimize database queries (use select_related/prefetch_related)
4. Maintain environment variable configuration
5. Follow Django best practices and PEP 8 style guide
6. Test all changes before committing
7. Update documentation as needed

---

## Documentation

Comprehensive documentation is available in the following files:

- QUICKSTART.md: Quick setup and testing guide
- IMPROVEMENTS.md: Detailed technical improvements documentation
- Django Official Documentation: https://docs.djangoproject.com/

---

## License

This project is developed for Souss Massa Business School. Usage rights and distribution are determined by school policies.

---

## Support and Maintenance

For issues, errors, or feature requests:

1. Review the IMPROVEMENTS.md and QUICKSTART.md documentation
2. Check Django official documentation
3. Review project settings in school/settings.py
4. Enable debug logging for detailed error information
5. Verify environment configuration in .env

---

## Version History

Version 2.0 (Current - April 2026):
- Security hardening with environment variable management
- Performance optimizations with pagination and query optimization
- Comprehensive error handling and logging
- Code quality improvements across all views
- Production-ready configuration
- REST API framework integration
- Static file compression with WhiteNoise
- Enhanced search with case-insensitive filtering

Version 1.0:
- Initial Django project setup
- Basic CMS functionality
- Admin dashboard
- News and events management
- Formation catalog
- User authentication

---

## Technical Notes

- Minimum Python version: 3.8
- Tested with Django 5.1.4
- Compatible with Windows, macOS, and Linux
- Requires database with transaction support
- Recommended: PostgreSQL for production
- Supports modern browsers (Chrome, Firefox, Safari, Edge)

---

Last Updated: April 20, 2026
Maintained by: Development Team
Status: Production Ready
