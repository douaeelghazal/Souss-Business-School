# Setup script for Souss Business School Website

Write-Host "=== Setting up Souss Business School Website ===" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
cd backend
pip install -r requirements.txt

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Create superuser
Write-Host "Creating superuser account..." -ForegroundColor Yellow
python manage.py createsuperuser

Write-Host "`nSetup complete! To start the server, run: python manage.py runserver" -ForegroundColor Green
