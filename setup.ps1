# Quick Setup Script for Windows PowerShell

Write-Host "🚀 Setting up RAG Document Q&A Application..." -ForegroundColor Cyan

# Backend Setup
Write-Host "`n📦 Setting up Backend..." -ForegroundColor Yellow
Set-Location -Path "backend"

Write-Host "Creating virtual environment..." -ForegroundColor Gray
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Gray
.\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Gray
pip install -r requirements.txt

Write-Host "`n⚠️  IMPORTANT: Please add your Groq API key to backend\.env" -ForegroundColor Red
Write-Host "Get your API key from: https://console.groq.com/" -ForegroundColor Yellow

# Return to root
Set-Location -Path ".."

# Frontend Setup
Write-Host "`n📦 Setting up Frontend..." -ForegroundColor Yellow
Set-Location -Path "frontend"

Write-Host "Installing Node dependencies..." -ForegroundColor Gray
npm install

Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "`nTo start the application:" -ForegroundColor Cyan
Write-Host "1. Backend: cd backend; python main.py" -ForegroundColor White
Write-Host "2. Frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host "`nAccess the app at: http://localhost:3000" -ForegroundColor Cyan

# Return to root
Set-Location -Path ".."
