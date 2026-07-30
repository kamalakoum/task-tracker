# Task Tracker — Architecture (Targeted Context)

## 1. What the app does

Task Tracker is a monolithic FastAPI backend that exposes task CRUD endpoints. It creates tasks with server-generated UUIDs and UTC timestamps, lists and filters tasks, retrieves individual tasks, updates them, and deletes them.

## 2. Data model

The central entity is `TaskResponse`, with `id`, `title`, `description`, `status`, `priority`, `assignee`, `created_at`, and `updated_at`.

`TaskCreate` accepts `title`, optional `description`, `status`, `priority`, and `assignee`; defaults are an empty description, `ToDo` status, `Medium` priority, and no assignee. `TaskUpdate` makes those mutable fields optional. Status values are `ToDo`, `InProgress`, and `Done`; priorities are `Low`, `Medium`, and `High`.

## 3. Request flow

For `POST /tasks`, FastAPI passes the request body to `TaskCreate`. The model validates and trims the title, rejects blank titles and titles longer than 200 characters, and rejects unknown fields. `create_task` calls `storage.add_task`, which generates a UUID and UTC timestamps, builds a `TaskResponse`, stores it in the process-local task dictionary, and returns it with HTTP 201.

## 4. Key files

- `app/main.py` — FastAPI application setup, CORS configuration, route registration, and task endpoints.
- `app/models.py` — task schemas, enums, defaults, and title validation.
- `app/storage.py` — in-memory task storage and CRUD functions.
- `app/business_rules.py` — imported for status-transition validation; implementation is not visible from the files I read.
- `app/routes/health.py` — health router is registered; behavior is not visible from the files I read.
- `app/routes/version.py` — version router is registered; behavior is not visible from the files I read.

## 5. Conventions

Validation is schema-based: create/update models forbid unknown fields, and titles are normalized by trimming whitespace. Storage is an in-memory module-level dictionary keyed by task ID, so persistence across process restarts is not visible from the files I read. Endpoint handlers raise HTTP 404 when storage reports a missing task; create returns HTTP 201 and delete is configured for HTTP 204. CORS explicitly permits several localhost origins and `null`; the actual frontend implementation and its request behavior are not visible from the files I read.

## 6. Not visible or assumptions

- Status-transition rules enforced by `validate_status_transition`.
- Health and version endpoint behavior.
- Frontend files, UI behavior, and API calls.
- Authentication, authorization, database configuration, deployment, logging, tests, and CI.
- Ordering guarantees for task lists.
