# Verification

## Baseline (before changes)
Command: `python -m pytest -q`  
Result: **19 passed**

## Backend tests (after comments + activity)
Command: `python -m pytest -q`  
Result: **36 passed**

New suites:
- `tests/test_comments.py`
- `tests/test_activity.py`

## Manual / API smoke checks
Used TestClient smoke script after pytest:
- Create task → `comment_count` starts at 0
- Add comment → listed under task comments
- Activity contains `task_created` then `comment_added`
- Delete comment → 204

Browser checks (with `uvicorn app.main:app --reload` + open `frontend/index.html`):
- [x] Activity panel loads on page open
- [x] Edit modal shows comments + task activity
- [x] Adding a comment updates card count and activity feed
- [x] Dragging a card creates `status_changed` activity

## Behavior contract (before → after)
| Behavior | Before | After |
|----------|--------|-------|
| Task CRUD | Supported | Unchanged |
| Status transitions | Enforced | Unchanged + activity event |
| Comments | N/A | Add/list/delete with validation |
| Activity | N/A | Global + per-task feeds |
| Task response body | No comment_count | Includes `comment_count` (default 0) |

## Break Test evidence
1. **Blank comment** — temporarily removed text validator expectation by posting `"text": "   "` → still 422 from model validation. Restored/confirmed test `test_add_comment_rejects_blank_text` fails if assertion expects 201.
2. **Invalid status transition still blocked** — `ToDo → Done` remains 422; activity does not record a status_changed event for rejected transitions.
