# Task Tracker

A lightweight FastAPI backend for tracking tasks, built as a simple monolithic
application for learning purposes. It prioritizes clarity and fast iteration.
Task data is stored in memory (not persisted across restarts).

## Final Project

- **Branch:** `final-project` (built on top of `mid-course-project`)
- **Scope:** mid-course features (comments + activity), CI, Docker, and release/AI evidence in `docs/`
- **Evidence:** [`docs/release-evidence.md`](docs/release-evidence.md), [`docs/final-ai-review.md`](docs/final-ai-review.md)

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
- Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response (timestamp will differ):

```json
{"status":"ok","timestamp":"2026-08-02T07:21:05.324632+00:00"}
```

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
python -m pytest -q
```

Verified result on this branch: `39 passed in 0.15s`.

Useful variants:

```bash
python -m pytest -v
python -m pytest -v --tb=short
python -m pytest tests/test_comments.py tests/test_activity.py
python -m pytest -k "comment or activity"
```

## How CI runs tests

Workflow: `.github/workflows/ci.yml`

```bash
pip install -r requirements.txt
pytest -v --tb=short
```

CI runs on every `push` and on `pull_request` to `main`. There is no `continue-on-error`, no `|| true`, and pytest is not skipped.

## How to run with Docker

```bash
docker build -t task-tracker-backend:final .
docker run --rm -d -p 8000:8000 --name task-tracker-final task-tracker-backend:final
curl http://127.0.0.1:8000/health
```

Expected `/health` response (timestamp will differ):

```json
{"status":"ok","timestamp":"2026-08-02T07:21:17.641693+00:00"}
```

Stop the container when finished:

```bash
docker stop task-tracker-final
```

The image runs as non-root user `app` and does not bake in any `.env` secrets.

## Evidence files

- [`docs/midcourse/`](docs/midcourse/) — mid-course user stories, ADR, prompt log, verification, reflection
- [`docs/release-evidence.md`](docs/release-evidence.md) — verified run commands, test output, CI and Docker checks
- [`docs/final-ai-review.md`](docs/final-ai-review.md) — AI review log, security findings, ownership statement
- [`docs/ai-playbook.md`](docs/ai-playbook.md) — personal AI usage rules and review workflow
- [`docs/security-review.md`](docs/security-review.md) — security findings with file evidence

## AI assistance summary

**What AI helped with:** drafting and reviewing README/CI/Docker documentation, grading security findings in `docs/security-review.md`, and debugging support during mid-course comments and activity work.

**How I verified the result:**

- Ran `python -m pytest -q` — 39 tests passed.
- Started the app with `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000` and confirmed `GET /health` returns 200.
- Built and ran the Docker image and confirmed `/health` returns 200 (see `docs/release-evidence.md`).
- Reviewed diffs before accepting changes and manually tested the Kanban UI (comments + activity feed).

**AI suggestions I rejected or corrected:**

1. **SQLite-backed storage (wrong)** — AI suggested describing the app as SQLite-backed. I rejected this after reading `app/storage.py`, which uses an in-memory dictionary. I corrected the README to match the code.
2. **Add auth/database to Docker (wrong)** — AI suggested adding a database or auth layer for the final project. I rejected this because it adds new product scope; the container stays a simple runtime wrapper.
3. **Simplify CI workflow (noise)** — AI suggested a looser CI setup. I kept `.github/workflows/ci.yml` as-is because it already runs `pytest -v --tb=short` reliably.

Full review grades and decisions are recorded in [`docs/final-ai-review.md`](docs/final-ai-review.md).
