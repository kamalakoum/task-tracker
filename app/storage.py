from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Args:
        payload: Task creation data with title and optional description, status,
            priority, and assignee.

    Returns:
        TaskResponse: The newly created task with auto-generated UUID, created_at,
            and updated_at both set to the current UTC time.
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
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

    updated = task.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    """Delete a task by its UUID.

    Args:
        task_id: UUID of the task to delete.

    Returns:
        bool: True if the task was found and deleted, False if task did not exist.
    """
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def _reset() -> None:
    _tasks.clear()
