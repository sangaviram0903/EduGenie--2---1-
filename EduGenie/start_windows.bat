@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python was not found in PATH. Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    py -3 -m venv .venv
)

set VENV_PY=%~dp0\.venv\Scripts\python.exe

echo Installing dependencies...
"%VENV_PY%" -m pip install --upgrade pip
"%VENV_PY%" -m pip install -r requirements.txt

if not exist ".env" (
    echo .env file is missing.
    echo Please create .env in the project root with your GEMINI_API_KEY before starting the app.
    echo Example:
    echo GEMINI_API_KEY=YOUR_API_KEY_HERE
    echo GEMINI_MODEL=gemini-3.6-flash
    pause
    exit /b 1
)

echo Starting EduGenie server...
start "EduGenie" cmd /k "%VENV_PY% -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

ping -n 12 127.0.0.1 >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; try { $resp = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8000/api/health'; Write-Host $resp.Content } catch { Write-Host 'Health check failed. The server may still be starting or there is an app error.'; exit 1 }"

echo.
echo App is running at: http://127.0.0.1:8000
echo API docs: http://127.0.0.1:8000/docs
pause
endlocal
