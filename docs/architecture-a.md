# Task Tracker Architecture

## What the app does

Task Tracker is a small monolithic FastAPI application that exposes a REST API to create, list, retrieve, update, and delete work tasks. A standalone static Kanban frontend loads and manages those tasks through the API.

## Data model

**Task**: `id` (server-generated UUID), `title` (required, trimmed, 1–200 characters), `description` (defaults to `""`), `status` (`ToDo`, `InProgress`, `Done`; default `ToDo`), `priority` (`Low`, `Medium`, `High`; default `Medium`), `assignee` (nullable), and server-generated UTC `created_at` / `updated_at` timestamps.

## Request flow: create a task

1. The frontend submits JSON to `POST /tasks` at `http://localhost:8000`.
2. FastAPI validates the body against `TaskCreate`.
3. `app.storage.add_task()` generates a UUID and UTC timestamps, constructs a response model, and stores it in the module-level dictionary.
4. The API returns the created task with HTTP 201; the frontend adds it to its in-browser board state.

## Key files

- `app/main.py` — FastAPI setup, CORS policy, task endpoints, and route registration.
- `app/models.py` — Pydantic request/response models, enums, defaults, and title validation.
- `app/storage.py` — In-memory task dictionary and CRUD operations.
- `app/business_rules.py` — Valid status-transition state machine.
- `app/routes/health.py` — `GET /health` operational check with UTC timestamp.
- `app/routes/version.py` — `GET /version` application-version response.
- `frontend/index.html` — Static Kanban UI, browser state, and API calls.
- `tests/test_tasks.py` — API behavior and validation coverage.
- `docs/decisions/in-memory-storage.md` — Rationale and limitations of ephemeral storage.

## Conventions

- **Validation:** Pydantic rejects unknown create/update fields and invalid enum values; blank or oversized titles return 422.
- **Storage:** Tasks live only in a process-local Python dictionary; they are lost on restart.
- **Errors:** Missing tasks return 404; validation failures and illegal status changes return 422. Allowed transitions are `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`.
- **Frontend/backend:** The frontend uses `fetch` against a fixed localhost API URL, loads all tasks with `GET /tasks`, and uses `POST`/`PATCH` for creation and edits or drag-and-drop moves.

## Not visible or assumptions

- Authentication, authorization, user accounts, and task ownership are not visible.
- Durable persistence, database migrations, concurrency control, pagination, and production deployment behavior are not confirmed.
- The README’s SQLite description conflicts with the current implementation, which uses in-memory storage.
- The frontend references `styles.css`, but that file is not present in the repository listing; the page also contains substantial inline styling.
