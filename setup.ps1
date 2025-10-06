# Cross-platform setup script for Triality-HDC (PowerShell)
# Sets up environment on Windows systems

Write-Host "Triality v2.0 - Cross-Platform Setup" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Using Python: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Activating..." -ForegroundColor Cyan
} else {
    python -m venv .venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Install requirements
Write-Host ""
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create results directory
Write-Host ""
Write-Host "Creating results directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "results" | Out-Null

Write-Host ""
Write-Host "=======================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the full pipeline:" -ForegroundColor Cyan
Write-Host "  Batch: .\run_full_pipeline.bat" -ForegroundColor White
Write-Host "  PowerShell: .\run_full_pipeline.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run individual components:" -ForegroundColor Cyan
Write-Host "  Metrics only (Batch): .\run_metrics.bat" -ForegroundColor White
Write-Host "  Metrics only (PowerShell): .\run_metrics.ps1" -ForegroundColor White
Write-Host "=======================================" -ForegroundColor Green
