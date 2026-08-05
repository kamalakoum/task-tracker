# User Stories

## Feature 1: Task comments

### US-C1 — Add a comment to a task
**As a** teammate, **I want** to leave a short note on a task **so that** discussion stays attached to the work item.

Acceptance criteria:
- Edit modal shows a comments section for existing tasks.
- Non-blank comment text creates a comment via `POST /tasks/{id}/comments` and returns 201.
- Blank/whitespace-only text is rejected with 422.
- Card comment count increases after a successful add.

**AI assumption corrected:** AI first suggested nesting comments inside `TaskResponse` and accepting comments on create. Corrected to separate comment endpoints and edit-modal-only UX to keep create payloads unchanged.

### US-C2 — View comments for a task
**As a** teammate, **I want** to see all comments on a task **so that** I can catch up before editing.

Acceptance criteria:
- Opening Edit loads comments from `GET /tasks/{id}/comments`.
- Comments render oldest-first with timestamps.
- Missing task returns 404.

### US-C3 — Delete a comment
**As a** teammate, **I want** to remove a mistaken comment **so that** the thread stays accurate.

Acceptance criteria:
- Delete button calls `DELETE /tasks/{id}/comments/{comment_id}` and returns 204.
- Missing task or missing comment returns 404.
- Comment count on the task decreases.

### US-C4 — Comments disappear with deleted tasks
**As a** system owner, **I want** comments removed when a task is deleted **so that** orphaned notes are not retained.

Acceptance criteria:
- Deleting a task cascades comment deletion from in-memory storage.
- Listing comments for that task afterward returns 404.

## Feature 2: Activity log

### US-A1 — See global activity
**As a** teammate, **I want** a board-side activity feed **so that** I can see recent changes without opening each task.

Acceptance criteria:
- Right-hand Activity panel loads `GET /activity`.
- Events show type, message, and timestamp newest-first.
- Refresh button reloads the feed.

**AI assumption corrected:** AI suggested persisting activity to SQLite and adding pagination/filters. Rejected as out of scope; kept the existing in-memory store pattern.

### US-A2 — Task create/update/delete create events
**As a** teammate, **I want** create/update/delete actions recorded **so that** history is auditable during a session.

Acceptance criteria:
- Creating a task emits `task_created`.
- Updating non-status fields emits `task_updated` with changed fields.
- Deleting a task emits `task_deleted` (kept intentionally even after task removal).

### US-A3 — Status changes include from/to
**As a** teammate, **I want** status moves to show previous and next status **so that** workflow changes are clear.

Acceptance criteria:
- Valid status transition emits `status_changed`.
- Event `details` include `from` and `to`.

### US-A4 — Task-specific activity in the edit modal
**As a** teammate, **I want** activity for the open task **so that** I can review that item’s history while editing.

Acceptance criteria:
- Edit modal loads `GET /tasks/{id}/activity`.
- Missing task returns 404.
- Comment add/delete also appear in the task activity list.
