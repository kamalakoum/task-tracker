# Prompt Log

## Feature 1: Task comments

### Prompt 1 (weak → rewritten)
**Weak:** “Add comments to tasks.”

**Stronger rewrite:** “Add task comments to this FastAPI app using the existing in-memory storage pattern. Endpoints: POST/GET `/tasks/{id}/comments` and DELETE `/tasks/{id}/comments/{comment_id}`. Validate non-blank trimmed text (max 1000). Return 404 for missing task/comment. Keep models in `app/models.py`, storage in `app/storage.py`, and add pytest coverage matching `tests/test_tasks.py` style.”

**AI returned:** Separate comment models, storage helpers, route module, and tests.

**Decision:** Accepted structure. Edited max length and cascade-delete behavior. Rejected nesting comments inside `TaskCreate`.

### Prompt 2
**Prompt:** “Wire comments into `frontend/index.html` edit modal with list/add/delete and show comment count on cards.”

**AI returned:** Modal panel + card badge + fetch helpers.

**Decision:** Accepted. Edited to hide comments panel in create mode and refresh activity after comment changes.

### Prompt 3
**Prompt:** “Write pytest cases for blank comment rejection, list order, delete 404s, and comment_count updates.”

**AI returned:** `tests/test_comments.py` covering those cases.

**Decision:** Accepted with minor assertion wording edits.

## Feature 2: Activity log

### Prompt 1
**Prompt:** “Record in-memory activity events for task create/update/status change/delete and comment add/delete. Expose GET `/activity` and GET `/tasks/{id}/activity`. Status events must include from/to.”

**AI returned:** `ActivityEvent` model, storage recorder, activity router, tests.

**Decision:** Accepted. Rejected SQLite persistence and actor/user fields as out of scope.

### Prompt 2 (weak → rewritten)
**Weak:** “Make an activity UI.”

**Stronger rewrite:** “Add a compact sticky Activity panel beside the Kanban board that loads GET `/activity`, plus a task activity section in the edit modal from GET `/tasks/{id}/activity`. Keep styling consistent with existing CSS variables.”

**AI returned:** Board layout + modal activity section + refresh button.

**Decision:** Accepted. Edited empty/error rendering to reuse one helper.

### Prompt 3
**Prompt:** “Add tests proving create/update/delete events and status_changed details.from/to.”

**AI returned:** `tests/test_activity.py`.

**Decision:** Accepted fully after running pytest (all green).
