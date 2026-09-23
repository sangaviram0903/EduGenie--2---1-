$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "Python was not found in PATH. Please install Python 3.10+ and try again."
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating Python virtual environment..."
    py -3 -m venv .venv
}

$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Installing dependencies..."
& $venvPy -m pip install --upgrade pip
& $venvPy -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host ".env file is missing."
    Write-Host "Please create .env in the project root with your GEMINI_API_KEY before starting the app."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting EduGenie server..."
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "$venvPy -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -WorkingDirectory $PSScriptRoot

Start-Sleep -Seconds 12

try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8000/api/health"
    Write-Host $resp.Content
} catch {
    Write-Host "Health check failed. The server may still be starting or there is an app error."
    exit 1
}

Write-Host ""
Write-Host "App is running at: http://127.0.0.1:8000"
Write-Host "API docs: http://127.0.0.1:8000/docs"
Read-Host "Press Enter to exit"
