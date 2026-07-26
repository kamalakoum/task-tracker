# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Task Tracker Backend** is a lightweight FastAPI-based REST API for tracking tasks. It's a deliberately simple monolithic application designed for learning purposes that prioritizes clarity and fast iteration over enterprise architecture. Data is stored in memory (not persisted to a database).

Key characteristics:
- Uses FastAPI for the web framework and routing
- Employs Pydantic for data validation
- Stores all task data in a module-level dictionary (in-memory)
- Enforces business rules like state machine transitions for task status
- Uses simple, direct SQLite-style thinking rather than ORM abstractions

## Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or: .\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy example if needed)
cp .env.example .env
```

### Running
```bash
# Start development server with auto-reload
uvicorn app.main:app --reload

# Server runs at http://127.0.0.1:8000
# API docs available at http://127.0.0.1:8000/docs
```

### Testing
```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run a single test file
python -m pytest tests/test_tasks.py

# Run a single test
python -m pytest tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body

# Run tests matching a pattern
python -m pytest -k "list_tasks"

# Run with coverage
python -m pytest --cov=app
```

## Architecture

### Module Structure

- **app/main.py** — Application entry point. Initializes FastAPI, sets up CORS middleware, and defines all route handlers (GET, POST, PATCH, DELETE for tasks). Also loads environment variables.

- **app/models.py** — Defines all Pydantic models:
  - `TaskStatus` (enum: ToDo, InProgress, Done)
  - `TaskPriority` (enum: Low, Medium, High)
  - `TaskCreate` — validation schema for POST /tasks
  - `TaskUpdate` — validation schema for PATCH /tasks/{id}
  - `TaskResponse` — schema for API responses
  - Title validation is centralized in `_normalize_title()`

- **app/storage.py** — In-memory data store. Manages a module-level `_tasks` dictionary. Provides functions:
  - `add_task()` — creates task with UUID and timestamps
  - `get_task_by_id()` — retrieves single task
  - `get_all_tasks()` — lists all with optional filtering by status/priority
  - `update_task()` — partial updates, preserves unset fields
  - `delete_task()` — removes task
  - `_reset()` — clears all tasks (used in tests)

- **app/business_rules.py** — Encodes workflow rules. Contains `VALID_TRANSITIONS` (frozenset of allowed status tuples) and `validate_status_transition()` function. This enforces the state machine: only specific transitions are allowed (e.g., ToDo → InProgress, but not ToDo → Done directly).

- **app/routes/health.py** — Health check endpoint (/health). Minimal route for deployment readiness.

- **tests/** — Full test suite using pytest:
  - `conftest.py` defines fixtures: `_reset_storage` (runs before/after each test), `client` (TestClient), `created_task` (helper task)
  - `test_tasks.py` covers all CRUD operations and business rule validation
  - Tests verify status codes, response bodies, filtering, transitions, and edge cases

### Request Flow

1. Client sends request to a route handler in `main.py`
2. FastAPI/Pydantic validates the request body against TaskCreate/TaskUpdate models
3. Handler calls functions from `app/storage`
4. For status changes, `business_rules.validate_status_transition()` is called
5. Storage function updates the in-memory `_tasks` dict and returns TaskResponse
6. FastAPI serializes response and returns JSON

### Data Model

All tasks have:
- `id` (UUID string, auto-generated)
- `title` (required, 1–200 chars, stripped)
- `description` (optional, defaults to empty string)
- `status` (TaskStatus enum, defaults to "ToDo")
- `priority` (TaskPriority enum, defaults to "Medium")
- `assignee` (optional string)
- `created_at` (UTC datetime, immutable)
- `updated_at` (UTC datetime, updated on every change)

### Key Design Patterns

**Validation at Entry** — Pydantic handles all input validation in `TaskCreate` and `TaskUpdate`. Invalid data is rejected with 422 status before reaching business logic.

**Separation of Concerns** — Business rules (state machine transitions) are isolated in `business_rules.py`, not mixed into route handlers or storage.

**Immutable Timestamps** — `created_at` is never modified; `updated_at` is always refreshed on updates using `model_copy()`.

**Partial Updates** — PATCH endpoint uses `model_dump(exclude_unset=True)` to only apply provided fields, leaving others unchanged.

**In-Memory Storage** — The `_tasks` dict is reset before/after each test, ensuring test isolation. In production, this would need to be replaced with a real database.

## Common Development Tasks

### Adding a new endpoint
1. Add Pydantic model(s) to `models.py` if needed
2. Add storage function to `storage.py`
3. Add route handler to `main.py`
4. Write tests in `tests/test_tasks.py`

### Adding a business rule
1. Add logic to `business_rules.py`
2. Call the validation function from the relevant route handler in `main.py`
3. Write tests covering valid and invalid scenarios

### Running a specific test while developing
Use `-k` for pattern matching or the full path: `python -m pytest tests/test_tasks.py::test_name -v`

## Dependencies

- **fastapi** — web framework
- **uvicorn** — ASGI server
- **pydantic** — data validation
- **python-dotenv** — environment variable loading
