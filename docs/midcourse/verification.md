# Verification

## Baseline (before changes)
Command: `python -m pytest -q`  
Output:

```text
.......................................                                  [100%]
39 passed in 0.20s
```

## Backend tests (after comments + activity)
Command: `python -m pytest -q`  
Result: **36 passed** (comments + activity added)

After optional extensions + midcourse packaging:
Command: `python -m pytest -q`  
Result: **39 passed** (includes `tests/test_bulk.py`)

New suites:
- `tests/test_comments.py` (10 tests)
- `tests/test_activity.py` (7 tests)
- `tests/test_bulk.py` (3 tests; optional extension)

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
The following are mutation tests against the working implementation. In each case,
the production code was changed temporarily, the existing test was run, and the
production code was restored. The assertions were not changed.

### 1. Blank comments must be rejected

Code changed temporarily in [app/models.py](../../app/models.py): removed the
`if not stripped` branch from `_normalize_comment_text()`:

```python
def _normalize_comment_text(value: str) -> str:
	stripped = value.strip()
	if len(stripped) > 1000:
		raise ValueError("comment text must be at most 1000 characters")
	return stripped
```

Command:

```text
python -m pytest tests/test_comments.py::test_add_comment_rejects_blank_text -q
```

Real failing output:

```text
F                                                                        [100%]
_____________________ test_add_comment_rejects_blank_text ______________________
>       assert response.status_code == 422
E       assert 201 == 422
E        +  where 201 = <Response [201 Created]>.status_code
=========================== short test summary info ============================
FAILED tests/test_comments.py::test_add_comment_rejects_blank_text - assert 201 == 422
1 failed in 0.03s
```

Restore: restored the `if not stripped` check and its
`ValueError("comment text must not be blank")` branch in
[app/models.py](../../app/models.py).

Restore command and passing output:

```text
python -m pytest tests/test_comments.py::test_add_comment_rejects_blank_text -q
.                                                                        [100%]
1 passed in 0.01s
```

### 2. `ToDo → Done` must remain forbidden

Code changed temporarily in [app/business_rules.py](../../app/business_rules.py):
added the forbidden transition to `VALID_TRANSITIONS`:

```python
VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
	(TaskStatus.TODO, TaskStatus.IN_PROGRESS),
	(TaskStatus.TODO, TaskStatus.DONE),  # temporary mutation
	(TaskStatus.IN_PROGRESS, TaskStatus.DONE),
	(TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})
```

Command:

```text
python -m pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -q
```

Real failing output:

```text
F                                                                        [100%]
____________ test_patch_invalid_transition_todo_to_done_returns_422 ____________
>       assert response.status_code == 422
E       assert 200 == 422
E        +  where 200 = <Response [200 OK]>.status_code
=========================== short test summary info ============================
FAILED tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 - assert 200 == 422
1 failed in 0.03s
```

Restore: removed the temporary `(TaskStatus.TODO, TaskStatus.DONE)` entry from
[app/business_rules.py](../../app/business_rules.py).

Restore command and passing output:

```text
python -m pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -q
.                                                                        [100%]
1 passed in 0.01s
```

### Final verification

Command:

```text
python -m pytest -q
```

Output:

```text
.......................................                                  [100%]
39 passed in 0.14s
```

## Optional extensions (second commit)
Command: `python -m pytest -q`  
Expected additions:
- `POST /tasks/bulk-delete` with partial-success payload `{deleted, not_found}`
- Frontend toolbar: status/priority filters, localStorage saved views, multi-select bulk delete
- Light toolbar entrance animation

Tests: `tests/test_bulk.py`
