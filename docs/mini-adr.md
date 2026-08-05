# Mini ADR — Comments + Activity Log

## Context
Extend the existing in-memory Task Tracker with two scoped features required by the Module assessment: **Task comments** and **Activity log**. Both must be usable in the Kanban frontend and covered by pytest.

## Decision

### Comments
- Separate resources under `/tasks/{task_id}/comments`.
- Models: `CommentCreate`, `CommentResponse`.
- Validation: trimmed non-blank text, max 1000 chars.
- Maintain `comment_count` on `TaskResponse` for card badges.
- Cascade-delete comments when a task is deleted.

### Activity
- Append-only in-memory event list.
- Endpoints: `GET /activity` and `GET /tasks/{task_id}/activity`.
- Event types: `task_created`, `task_updated`, `status_changed`, `task_deleted`, `comment_added`, `comment_deleted`.
- Status-change events always include `from` / `to` in `details`.
- Delete events are **kept** after task deletion so the global feed remains useful.

### Frontend
- Comment count on cards.
- Comments + task activity inside the edit modal.
- Global activity panel beside the board.

## Alternatives considered / rejected
| Suggestion | Why rejected |
|------------|--------------|
| SQLite / ORM persistence | Conflicts with current in-memory architecture and overbuilds scope |
| Embed comments array in every task payload | Couples list responses to comment volume; breaks simple task schema |
| Full audit service with pagination, actors, auth | Too large for this assessment |
| Soft-delete comments | Unnecessary complexity for in-memory learning app |

## Consequences
- Activity and comments reset with process restart (same as tasks).
- Global activity retains deleted-task history for the current process lifetime.
- Frontend depends on CORS already configured for local static hosting.
