# Task Tracker Architecture

## What the app does

Task Tracker is a small monolithic FastAPI application for creating, listing, retrieving, updating, and deleting tasks. A standalone Kanban-style browser frontend groups tasks into To Do, In Progress, and Done columns and calls the API at http://localhost:8000.

## Data model

The primary entity is Task:

- id: server-generated UUID string.
- title: required, trimmed, non-blank, maximum 200 characters.
- description: string; defaults to `""`.
- status: ToDo, InProgress, or Done; defaults to ToDo.
- priority: Low, Medium, or High; defaults to Medium.
- assignee: optional string; defaults to null.
- created_at, updated_at: server-generated UTC timestamps.

Create and update request models accept only client-managed fields; response models include the server-managed fields.

## Request flow: create a task

The frontend submits a JSON `POST /tasks` request to the FastAPI app. FastAPI validates the payload against `TaskCreate`, including title normalization and enum validation. The route calls `storage.add_task`. Storage generates a UUID and UTC timestamps, builds a `TaskResponse`, and stores it in an in-memory dictionary keyed by ID. The API returns the task with HTTP 201; the frontend refreshes its task list and renders the updated board.

## Key files

- `app/main.py`: FastAPI application setup, CORS configuration, task endpoints, and router registration.
- `app/models.py`: Pydantic task request/response models, enums, defaults, and title validation.
- `app/storage.py`: In-memory task CRUD operations, UUID creation, and timestamps.
- `app/business_rules.py`: Allowed task-status transition rules.
- `app/routes/health.py`: `GET /health` endpoint.
- `app/routes/version.py`: `GET /version` endpoint.
- `frontend/index.html`: Standalone Kanban UI and browser-side API calls.
- `tests/test_tasks.py`: API behavior coverage for task CRUD, validation, filtering, and transitions.

## Conventions

Validation is schema-led with Pydantic; unknown request fields are rejected. Storage is a process-local Python dictionary, so tasks are lost when the application restarts. Missing task IDs return HTTP 404; invalid input and invalid status transitions return HTTP 422. Permitted transitions are ToDo → InProgress, InProgress → Done, and Done → InProgress. The frontend uses fetch to call the backend, renders server responses, and displays request errors in the UI. CORS allows selected local frontend origins.

## Not visible or assumptions

No file-summary list was supplied, so this draft relies on the provided AGENTS.md and inspected repository files. Authentication, authorization, database persistence, deployment workflow, CI, and production hosting are not confirmed. The README’s SQLite description conflicts with the current in-memory implementation, so source code is treated as authoritative.

## Which context item helped most

AGENTS.md helped most: it supplied the authoritative behavioral rules and highlighted the README-versus-source storage mismatch, which inspection of `app/storage.py` confirmed.

## Remaining assumptions or unsupported details

No architecture assumptions were added. The missing file-summary list, deployment/CI, authentication, and persistence beyond process memory remain unconfirmed.
