# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A
- Simple concept explanations
- 3-question MCQ quiz generation
- Educational passage summarization
- Beginner/intermediate/advanced learning paths
- A simple responsive HTML/CSS/JavaScript frontend
- FastAPI REST endpoints

## Important modernization

The supplied document was written around Gemini 1.5 Pro and the older Gemini Python SDK. Gemini 1.5 Pro was shut down on September 29, 2025, so this implementation uses the current Google Gen AI Python SDK and a currently available stable Gemini model instead.

The project keeps the documented module structure and the LaMini-Flan-T5 explanation idea, but makes local explanation optional so a new developer can run the full application without waiting for a large local model download.

## Project structure

```text
EduGenie/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── schemas.py
│   ├── gemini_service.py
│   ├── local_explanation.py
│   ├── explanation_module.py
│   ├── qna.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   ├── learning_path.py
│   └── main.py
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Prerequisites

- Python 3.10+
- VS Code
- A Gemini API key from Google AI Studio
- Internet connection for Gemini API calls
- Windows/macOS/Linux

## 2. Open the project in VS Code

Extract the project ZIP, then open the `EduGenie` folder in VS Code.

Open:

```text
Terminal → New Terminal
```

## 3. Create a virtual environment

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can instead run:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

and use `.venv\Scripts\python.exe` for the remaining commands.

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`torch` and `transformers` are included because the documented LaMini local explanation module is implemented. The default provider is Gemini, so the local model is not downloaded until you enable it.

## 5. Configure Gemini

Copy:

```text
.env.example
```

to:

```text
.env
```

Then edit `.env`:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-2.5-flash
EXPLANATION_PROVIDER=gemini
```

Do not commit `.env` to Git.

## 6. Run the application

From the project root:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 7. Test the application

### Browser

Try:

1. Ask a Question → `What is the largest ocean on Earth?`
2. Explain → `Pythagorean theorem`
3. Generate Quiz → paste a paragraph about a subject
4. Summarize → paste a long educational paragraph
5. Learning Path → `SQL`, choose `Beginner`

### API

Health check:

```bash
curl http://127.0.0.1:8000/api/health
```

Q&A:

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"What is the largest ocean on Earth?\"}"
```

PowerShell alternative:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/qa `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"What is the largest ocean on Earth?"}'
```

## 8. Run automated tests

With the virtual environment active:

```bash
pytest
```

The included tests intentionally cover the local application shell and health endpoint without making paid/remote Gemini calls.

## 9. Optional local LaMini explanation

The supplied documentation specifies `LaMini-Flan-T5-783M` for concept explanations.

To use it:

```env
EXPLANATION_PROVIDER=local
```

Start the app and call Explain. Hugging Face Transformers will download the model the first time it is needed.

For a hybrid mode:

```env
EXPLANATION_PROVIDER=auto
```

The app first tries the local model and falls back to Gemini if the local model cannot be loaded.

## 10. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web frontend |
| GET | `/api/health` | Health/configuration status |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | Generate 3 MCQs |
| POST | `/summarize` | Summarize educational text |
| POST | `/learn/recommendations` | Learning path |

## 11. Architecture

```text
Browser
   │
   ▼
HTML + CSS + JavaScript
   │
   ▼
FastAPI
   ├── /qa ───────────────► Gemini
   ├── /explain ──────────► LaMini (optional) / Gemini
   ├── /quiz ─────────────► Gemini + JSON validation
   ├── /summarize ────────► Gemini
   └── /learn/recommendations ► Gemini
```

## 12. Security notes

- Keep the Gemini key only in `.env`.
- Never put the API key in frontend JavaScript.
- Restrict `CORS_ORIGINS` when deploying.
- Add authentication and rate limiting before public deployment.
- Do not send sensitive student information to an external model without an appropriate privacy review.
- AI output should be checked for important academic decisions.

## 13. Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart Uvicorn after changing `.env`.

### `ModuleNotFoundError`

Make sure the virtual environment is active and run:

```bash
pip install -r requirements.txt
```

### Port 8000 is already in use

Run:

```bash
uvicorn app.main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### Local LaMini model is slow

Set:

```env
EXPLANATION_PROVIDER=gemini
```

The local model is CPU-based in this implementation, matching the documentation's lightweight/local approach. GPU acceleration can be added later if required.

## 14. Suggested future extensions

The supplied documentation identifies future possibilities such as voice interaction, multilingual support, mobile apps, progress tracking, gamification, adaptive learning, group study, teacher/parent dashboards, LMS integration, and image/PDF input. Those are intentionally not added to the base implementation so the delivered project remains aligned with the documented core scope.
