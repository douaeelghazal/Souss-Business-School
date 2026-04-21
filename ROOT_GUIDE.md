# Root Directory Guide

## Understanding Your Project Root

When you open the project, you'll see these folders and files. Here's what each does:

---

## 📁 Main Folders

### `backend/` - Django Server Code ⭐
**What's inside:** All Python/Django code, database, settings
```
backend/
├── manage.py              ← Start here for Django commands
├── requirements.txt       ← Python packages (install with pip)
├── data/db.sqlite3        ← Development database
├── ecole/                 ← Django settings
├── school/                ← Django configuration
└── playground/            ← Main app (models, views, templates)
```

**Why separate?**
- Keeps all server code together
- Easy to deploy just the backend
- Clear what's Python vs static files

**Start here:** `cd backend` then `python manage.py runserver`

---

### `frontend/` - Frontend Assets ⭐
**What's inside:** All images, documents, and compiled static files
```
frontend/
├── media/                 ← User uploads (images, documents)
├── staticfiles/           ← Production compiled CSS/JS
└── assets/                ← Organized assets for future use
```

**Why separate?**
- Can be served from CDN in production
- Easy to manage user uploads
- Clear what's frontend vs backend

**Note:** These folders are ignored by Git (.gitignore)

---

### `docs/` - Documentation 📖
**What's inside:** Setup guides and structure documentation
```
docs/
├── SETUP.md               ← How to set up the project
├── STRUCTURE.md           ← Folder organization details
└── TREE.md                ← Visual directory tree
```

**Read this first** when setting up the project

---

### `scripts/` - Automation Scripts 🔧
**What's inside:** PowerShell scripts for common tasks
```
scripts/
├── setup.ps1              ← Run this first: .\scripts\setup.ps1
└── runserver.ps1          ← Start server: .\scripts\runserver.ps1
```

**Why use scripts?**
- No need to remember commands
- Automation handles environment setup
- One-click development

---

### `.venv/` - Python Environment
**What's inside:** Installed Python packages (virtual environment)

**Important:** This folder is NOT tracked by Git
- Size: ~500MB (typical)
- Don't commit it
- It's auto-created by setup script

**Activate it:**
```bash
.\.venv\Scripts\Activate.ps1
```

---

### `.git/` - Version Control
**What's inside:** Git repository history

**Ignore:** You don't edit this folder directly

---

## 📄 Configuration Files

### `.env` - Local Environment Settings ⚡
**What's inside:** Your local configuration (secrets, settings)

**Example:**
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=...
EMAIL_HOST_PASSWORD=...
```

**Important:**
- ⛔ Never commit this file
- 📝 Create it from `.env.example`
- 🔐 Keep it secure (contains passwords)

**Status:** Your local copy (not in Git)

---

### `.env.example` - Settings Template 📋
**What's inside:** Template for `.env` file

**Purpose:**
- Shows what settings are needed
- Safe to commit to Git (no secrets)
- Use as template: `cp .env.example .env`

**Status:** Committed to Git

---

### `.gitignore` - Git Ignore Rules 🚫
**What's inside:** Files to ignore in version control

**Ignores:**
```
.env                    ← Local secrets
.venv/                  ← Virtual environment
__pycache__/            ← Python cache
backend/data/           ← Database
frontend/media/         ← User uploads
frontend/staticfiles/   ← Compiled files
```

**Status:** Committed to Git

---

## 📖 Documentation Files

### `README.md` - Original Project README
- Full project description
- Key features
- Architecture details

### `PROJECT_OVERVIEW.md` - Quick Reference 
- Navigation guide
- Quick start commands
- Technology stack

### `ORGANIZATION_SUMMARY.md` - What's New
- Reorganization summary
- Before/after comparison
- Improvement highlights

### `QUICKSTART.md` - Getting Started
- Quick start guide
- Common commands
- Troubleshooting

### `IMPROVEMENTS.md` - Enhancement Ideas
- Potential improvements
- Feature ideas
- Known issues

---

## 🎯 What To Do First

### 1. Read Documentation
Start with one of these:
- Quick: `PROJECT_OVERVIEW.md`
- Detailed: `docs/SETUP.md`
- Visual: `docs/TREE.md`

### 2. Set Up Environment
```bash
cp .env.example .env
.\scripts\setup.ps1
```

### 3. Start Development
```bash
.\scripts\runserver.ps1
```

### 4. Access Application
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin/

---

## 🔄 Common Workflows

### First Time Setup
```bash
.\scripts\setup.ps1
```

### Daily Development
```bash
.\.venv\Scripts\Activate.ps1
cd backend
python manage.py runserver
```

### Create Admin User
```bash
cd backend
python manage.py createsuperuser
```

### Collect Static Files (Production)
```bash
cd backend
python manage.py collectstatic
```

### Database Migration
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

---

## 📊 Key Concepts

### Backend vs Frontend
- **Backend** (`backend/`) - Python/Django server code
- **Frontend** (`frontend/`) - Static assets & user uploads

### Static Files
- **Development:** `backend/playground/static/` (auto-served)
- **Production:** `frontend/staticfiles/` (compiled via collectstatic)

### Database
- **Location:** `backend/data/db.sqlite3` (SQLite for dev)
- **Production:** Use PostgreSQL (configure via DATABASE_URL)

### Virtual Environment
- **Why:** Keep Python packages isolated per project
- **Where:** `.venv/` folder
- **Activate:** `.\.venv\Scripts\Activate.ps1`

---

## 🆘 Troubleshooting

### Can't activate .venv?
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### Port 8000 in use?
```bash
cd backend
python manage.py runserver 8001
```

### Need fresh database?
```bash
Remove-Item backend/data/db.sqlite3
cd backend
python manage.py migrate
```

### Missing dependencies?
```bash
cd backend
pip install -r requirements.txt
```

---

## 📚 File Organization

| Location | Type | Status | Notes |
|----------|------|--------|-------|
| `backend/` | Folder | Committed | Python/Django code |
| `frontend/` | Folder | Committed* | *media ignored by git |
| `docs/` | Folder | Committed | Documentation |
| `scripts/` | Folder | Committed | Setup scripts |
| `.venv/` | Folder | ❌ Ignored | Virtual environment |
| `.env` | File | ❌ Ignored | Local secrets |
| `.env.example` | File | ✅ Committed | Settings template |
| `.gitignore` | File | ✅ Committed | Git ignore rules |

---

## ✨ Summary

Your project is organized as:
1. **Server code** in `backend/`
2. **Assets** in `frontend/`
3. **Documentation** in `docs/`
4. **Scripts** in `scripts/`
5. **Config files** at root

**Next Step:** Read `docs/SETUP.md` and run `.\scripts\setup.ps1`

🚀 **Happy coding!**
