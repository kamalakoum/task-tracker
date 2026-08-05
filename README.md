# Task Tracker Backend

A lightweight FastAPI backend for tracking tasks, built as a simple monolithic
application for learning purposes. It prioritizes clarity and fast iteration.
Task data is stored in memory (not persisted across restarts).

## Mid-course features

This branch (`mid-course-project`) includes:

- **Task comments** — add, list, and delete comments on a task
- **Activity log** — global and per-task activity events
- **Optional extensions** — bulk delete, saved filter views (browser localStorage), light UI polish

Assessment docs live in [`docs/midcourse/`](docs/midcourse/).

## Setup

### 1. Create a virtual environment and install dependencies

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and adjust values if needed:

**Linux/macOS:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Do not commit real secrets. `.env` is for local config only; use `.env.example` as the template.

## Run the backend

```bash
source venv/bin/activate   # if not already active
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: `curl http://127.0.0.1:8000/health`

## Open the frontend

Keep the backend running, then in a second terminal:

```bash
cd frontend
python3 -m http.server 5500
```

Open http://127.0.0.1:5500 in your browser.

You can also open `frontend/index.html` directly in a browser. The UI calls `http://localhost:8000`.

## Run tests

```bash
source venv/bin/activate
pytest
```

Useful variants:

```bash
pytest -v
pytest tests/test_comments.py tests/test_activity.py
pytest -k "comment or activity"
```
