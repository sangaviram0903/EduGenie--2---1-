# EduGenie Setup Guide for Another PC

This guide explains exactly what to install and how to start the project on a new Windows computer.

## 1. Install required software

### Install Python

Use Python 3.10 or newer.

Recommended:
- Python 3.11
- Python 3.12

Download from:
https://www.python.org/downloads/

During installation, make sure to check:
- Add Python to PATH

### Install VS Code (optional but recommended)

Download from:
https://code.visualstudio.com/

### Install Git (optional)

If you want to clone the project instead of using a ZIP file.

Download from:
https://git-scm.com/downloads

---

## 2. Extract the project

If you received this project as a ZIP file:

1. Extract it to a folder like:
   C:\Projects\EduGenie

2. Open that folder in VS Code.

3. Open the terminal in VS Code:
   - Terminal -> New Terminal

---

## 3. Create a virtual environment

From the project root, run:

```powershell
py -3 -m venv .venv
```

Then activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

Then keep using the virtual environment Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 4. Install project dependencies

Inside the project folder with the virtual environment active:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs packages such as:
- FastAPI
- Uvicorn
- Jinja2
- Pydantic
- Google Gen AI SDK
- Transformers
- PyTorch
- pytest

---

## 5. Set up environment variables

Create a file named `.env` in the project root if it does not already exist.

Example content:

```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
GEMINI_MODEL=gemini-3.6-flash
EXPLANATION_PROVIDER=gemini
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
MAX_INPUT_CHARS=20000
MAX_QUIZ_QUESTIONS=5
CORS_ORIGINS=*
```

Important:
- Replace `YOUR_API_KEY_HERE` with your actual Google Gemini API key.
- You can get the key from Google AI Studio.
- Do not share the `.env` file publicly.

---

## 6. Start the project

From the project root:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

If `uvicorn` is not recognized, use:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Or if the virtual environment is active:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open in browser:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

---

## 7. Run tests

From the project root:

```powershell
pytest
```

Or:

```powershell
python -m pytest
```

---

## 8. Common issues and fixes

### Issue: `GEMINI_MODEL` no longer works

Use this model:

```env
GEMINI_MODEL=gemini-3.6-flash
```

### Issue: `TemplateResponse` error

This project is already fixed for the current FastAPI/Starlette versions, but if the code was changed, use the current template pattern:

```python
return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"app_name": settings.app_name},
)
```

### Issue: package installation fails

Try:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## 9. Quick copy-paste setup commands

```powershell
cd path\to\EduGenie
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Then create `.env` with the values above, then:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 10. Summary

To start the project on a new PC, you need:
- Python 3.10+
- Virtual environment
- pip install from requirements.txt
- `.env` with Gemini API key
- run uvicorn

Once these steps are complete, the app should run on:

```text
http://127.0.0.1:8000
```
