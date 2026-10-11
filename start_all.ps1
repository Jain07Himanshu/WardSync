# WardSync Unified Platform PowerShell Launcher
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "               WARDSYNC: CIVIC DISCOVERY & ACTION PLATFORM" -ForegroundColor Cyan
Write-Host "        Connecting civic_engine + civic_pipeline + wardsync-frontend" -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot
if (-not $root) { $root = Get-Location }

Write-Host "Launching Unified Backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; python run.py"

Start-Sleep -Seconds 2

Write-Host "Launching Frontend on http://localhost:5173 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\wardsync-frontend'; npm run dev"

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "All WardSync services launched!" -ForegroundColor Green
Write-Host "- Backend API & Swagger: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host "- Frontend Interactive:  http://localhost:5173" -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
