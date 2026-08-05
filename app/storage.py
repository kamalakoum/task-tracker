from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import (
    ActivityEvent,
    ActivityEventType,
    CommentCreate,
    CommentResponse,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_tasks: dict[str, TaskResponse] = {}
_comments: dict[str, CommentResponse] = {}
_activity: list[ActivityEvent] = []


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _record_activity(
    task_id: str,
    event_type: ActivityEventType,
    message: str,
    details: Optional[dict[str, str]] = None,
) -> ActivityEvent:
    event = ActivityEvent(
        id=str(uuid4()),
        task_id=task_id,
        event_type=event_type,
        message=message,
        details=details,
        created_at=_now(),
    )
    _activity.append(event)
    return event


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Args:
        payload: Task creation data with title and optional description, status,
            priority, and assignee.

    Returns:
        TaskResponse: The newly created task with auto-generated UUID, created_at,
            and updated_at both set to the current UTC time.
    """
    now = _now()
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        comment_count=0,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    _record_activity(
        task_id,
        ActivityEventType.TASK_CREATED,
        f'Task "{payload.title}" created',
        details={"title": payload.title, "status": payload.status.value},
    )
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """Retrieve all tasks with optional filtering.

    Args:
        status: Optional filter by task status (ToDo, InProgress, Done).
        priority: Optional filter by task priority (Low, Medium, High).

    Returns:
        list[TaskResponse]: All stored tasks, filtered by status and/or priority
            if specified. Returns empty list if no tasks match.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Retrieve a single task by its UUID.

    Args:
        task_id: UUID string of the task to retrieve.

    Returns:
        TaskResponse: The task if found, None otherwise.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Update an existing task with provided fields.

    Args:
        task_id: UUID of the task to update.
        payload: Partial update data; only provided fields are applied, others unchanged.

    Returns:
        TaskResponse: The updated task with refreshed updated_at timestamp if found,
            None if task does not exist.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    previous_status = task.status
    updated = task.model_copy(update={**updates, "updated_at": _now()})
    _tasks[task_id] = updated

    changed_fields = sorted(updates.keys())
    if "status" in updates and updates["status"] != previous_status:
        _record_activity(
            task_id,
            ActivityEventType.STATUS_CHANGED,
            f"Status changed from {previous_status.value} to {updates['status'].value}",
            details={
                "from": previous_status.value,
                "to": updates["status"].value,
            },
        )
        changed_fields = [field for field in changed_fields if field != "status"]

    if changed_fields:
        _record_activity(
            task_id,
            ActivityEventType.TASK_UPDATED,
            f"Task updated ({', '.join(changed_fields)})",
            details={field: str(updates[field]) for field in changed_fields},
        )

    return updated


def delete_task(task_id: str) -> bool:
    """Delete a task by its UUID.

    Args:
        task_id: UUID of the task to delete.

    Returns:
        bool: True if the task was found and deleted, False if task did not exist.
    """
    task = _tasks.get(task_id)
    if task is None:
        return False

    title = task.title
    del _tasks[task_id]

    comment_ids = [cid for cid, comment in _comments.items() if comment.task_id == task_id]
    for comment_id in comment_ids:
        del _comments[comment_id]

    _record_activity(
        task_id,
        ActivityEventType.TASK_DELETED,
        f'Task "{title}" deleted',
        details={"title": title},
    )
    return True


def add_comment(task_id: str, payload: CommentCreate) -> Optional[CommentResponse]:
    """Add a comment to a task.

    Returns:
        CommentResponse if the task exists, None if the task is missing.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    comment = CommentResponse(
        id=str(uuid4()),
        task_id=task_id,
        text=payload.text,
        created_at=_now(),
    )
    _comments[comment.id] = comment
    _tasks[task_id] = task.model_copy(
        update={"comment_count": task.comment_count + 1, "updated_at": _now()}
    )
    _record_activity(
        task_id,
        ActivityEventType.COMMENT_ADDED,
        "Comment added",
        details={"comment_id": comment.id},
    )
    return comment


def get_comments_for_task(task_id: str) -> Optional[list[CommentResponse]]:
    """List comments for a task ordered by created_at ascending.

    Returns:
        list of comments if the task exists, None if the task is missing.
    """
    if task_id not in _tasks:
        return None
    comments = [comment for comment in _comments.values() if comment.task_id == task_id]
    comments.sort(key=lambda item: item.created_at)
    return comments


def delete_comment(task_id: str, comment_id: str) -> Optional[bool]:
    """Delete a comment from a task.

    Returns:
        True if deleted, False if comment missing, None if task missing.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    comment = _comments.get(comment_id)
    if comment is None or comment.task_id != task_id:
        return False

    del _comments[comment_id]
    new_count = max(0, task.comment_count - 1)
    _tasks[task_id] = task.model_copy(update={"comment_count": new_count, "updated_at": _now()})
    _record_activity(
        task_id,
        ActivityEventType.COMMENT_DELETED,
        "Comment deleted",
        details={"comment_id": comment_id},
    )
    return True


def get_activity(task_id: Optional[str] = None) -> list[ActivityEvent]:
    """Return activity events newest-first, optionally filtered by task_id."""
    events = _activity
    if task_id is not None:
        events = [event for event in events if event.task_id == task_id]
    return sorted(events, key=lambda item: item.created_at, reverse=True)


def get_task_activity(task_id: str) -> Optional[list[ActivityEvent]]:
    """Return activity for a task if it exists; None if the task is missing."""
    if task_id not in _tasks:
        return None
    return get_activity(task_id=task_id)


def _reset() -> None:
    _tasks.clear()
    _comments.clear()
    _activity.clear()
