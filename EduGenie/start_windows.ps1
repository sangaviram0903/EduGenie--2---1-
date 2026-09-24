$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$pythonCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = 'py'
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = 'python'
}

if (-not $pythonCmd) {
    Write-Host "Python was not found in PATH. Please install Python 3.10+ and try again."
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating Python virtual environment..."
    if ($pythonCmd -eq 'py') {
        & py -3 -m venv .venv
    } else {
        & python -m venv .venv
    }
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
Start-Process -FilePath $venvPy -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload") -WorkingDirectory $PSScriptRoot -NoNewWindow

Start-Sleep -Seconds 12

$healthReady = $false
for ($attempt = 1; $attempt -le 30; $attempt++) {
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8000/api/health"
        $healthReady = $true
        break
    } catch {
        Start-Sleep -Seconds 2
    }
}

if (-not $healthReady) {
    Write-Host "Health check failed. The server may still be starting or there is an app error."
    exit 1
}

Write-Host $resp.Content

Write-Host ""
Write-Host "App is running at: http://127.0.0.1:8000"
Write-Host "API docs: http://127.0.0.1:8000/docs"
Read-Host "Press Enter to exit"
