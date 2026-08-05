# Task Tracker — Final Project

Branch: `final-project` (built on top of `mid-course-project`)

A lightweight FastAPI backend for tracking tasks, built as a simple monolithic
application for learning purposes. It prioritizes clarity and fast iteration.
Task data is stored in memory (not persisted across restarts).

## Features included from mid-course

- **Task comments** — add, list, and delete comments on a task
- **Activity log** — global and per-task activity events
- **Optional extensions** — bulk delete, saved filter views (browser localStorage), light UI polish

Mid-course assessment docs: [`docs/midcourse/`](docs/midcourse/)

## What this submission demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- Mid-course features (comments + activity) are included in this branch.
- CI runs the pytest suite on push and/or pull request.
- Docker image builds and runs with `/health` returning 200.
- AI review, security, and ownership evidence is in `docs/`.

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

## How to run locally

```bash
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: `curl http://127.0.0.1:8000/health`

### Open the frontend

Keep the backend running, then in a second terminal:

```bash
cd frontend
python3 -m http.server 5500
```

Open http://127.0.0.1:5500 in your browser.

You can also open `frontend/index.html` directly. The UI calls `http://localhost:8000`.

## How to run tests

```bash
source venv/bin/activate
pytest
```

Useful variants:

```bash
pytest -v
pytest -v --tb=short
pytest tests/test_comments.py tests/test_activity.py
pytest -k "comment or activity"
```

## How to run with Docker

```bash
docker build -t task-tracker-backend:final .
docker run --rm -d -p 8000:8000 --name task-tracker-final task-tracker-backend:final
curl http://127.0.0.1:8000/health
```

Stop the container when finished:

```bash
docker stop task-tracker-final
```

## Evidence files

- [`docs/midcourse/`](docs/midcourse/) — mid-course user stories, ADR, prompt log, verification, reflection
- [`docs/release-evidence.md`](docs/release-evidence.md)
- [`docs/final-ai-review.md`](docs/final-ai-review.md)
- [`docs/ai-playbook.md`](docs/ai-playbook.md)

## AI assistance summary

AI helped draft or review CI/Docker docs, security notes, and debugging support during mid-course feature work.

I verified the work by running pytest, reviewing diffs, exercising Docker `/health`, and manually testing the Kanban UI (comments + activity).

One AI suggestion I rejected or corrected: describing the app as SQLite-backed — the real store is an in-memory dictionary in `app/storage.py`.
