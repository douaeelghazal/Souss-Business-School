# Run development server script

Write-Host "Starting Souss Business School Website..." -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Start server
cd backend
python manage.py runserver
