# Application entry point: creates the FastAPI instance and loads environment
# variables. Run with: uvicorn app.main:app --reload
import os

from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage, __version__
from app.business_rules import validate_status_transition
from app.models import (
    BulkDeleteRequest,
    BulkDeleteResponse,
    TaskCreate,
    TaskResponse,
    TaskStatus,
    TaskPriority,
    TaskUpdate,
)
from app.routes.activity import router as activity_router
from app.routes.comments import router as comments_router
from app.routes.health import router as health_router
from app.routes.version import router as version_router

# Load environment variables from .env (falls back to defaults if absent)
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

# Create the FastAPI application instance
app = FastAPI(
    title="Task Tracker Backend",
    description="A simple monolithic FastAPI backend for tracking tasks.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# Register routes
app.include_router(health_router)
app.include_router(version_router)
app.include_router(comments_router)
app.include_router(activity_router)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: Task creation data including title, optional description, status,
            priority, and assignee.

    Returns:
        TaskResponse: The created task with auto-generated id, created_at, and updated_at.

    Raises:
        HTTPException: 422 if payload validation fails (e.g., title is blank or exceeds
            200 characters).

    Example:
        POST /tasks
        {"title": "Buy groceries", "priority": "High"}
        Response: {"id": "...", "title": "Buy groceries", ...}
    """
    return storage.add_task(payload)


@app.post("/tasks/bulk-delete", response_model=BulkDeleteResponse, tags=["tasks"])
def bulk_delete_tasks(payload: BulkDeleteRequest) -> BulkDeleteResponse:
    """Delete multiple tasks in one request.

    Partial success is allowed: missing ids are returned in `not_found`
    while existing ids are deleted and listed in `deleted`.
    """
    deleted, not_found = storage.bulk_delete_tasks(payload.task_ids)
    return BulkDeleteResponse(deleted=deleted, not_found=not_found)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """List all tasks with optional filtering.

    Args:
        status: Optional task status filter (ToDo, InProgress, Done).
        priority: Optional task priority filter (Low, Medium, High).

    Returns:
        list[TaskResponse]: List of tasks matching the filters (empty if no matches).

    Example:
        GET /tasks?status=InProgress&priority=High
        Response: [{"id": "...", "title": "...", ...}, ...]
    """
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by ID.

    Args:
        task_id: UUID of the task to retrieve.

    Returns:
        TaskResponse: The requested task.

    Raises:
        HTTPException: 404 if the task does not exist.

    Example:
        GET /tasks/550e8400-e29b-41d4-a716-446655440000
        Response: {"id": "550e8400-e29b-41d4-a716-446655440000", "title": "...", ...}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Update an existing task.

    Args:
        task_id: UUID of the task to update.
        payload: Partial task update data (only provided fields are updated).

    Returns:
        TaskResponse: The updated task with refreshed updated_at timestamp.

    Raises:
        HTTPException: 404 if the task does not exist.
        HTTPException: 422 if the status transition is invalid (e.g., Done -> ToDo).

    Example:
        PATCH /tasks/550e8400-e29b-41d4-a716-446655440000
        {"status": "InProgress"}
        Response: {"id": "...", "status": "InProgress", "updated_at": "...", ...}
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by ID.

    Args:
        task_id: UUID of the task to delete.

    Raises:
        HTTPException: 404 if the task does not exist.

    Example:
        DELETE /tasks/550e8400-e29b-41d4-a716-446655440000
        Response: 204 No Content
    """
    if storage.delete_task(task_id):
        return
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")



# @app.on_event("shutdown")   
# async def shutdown_event() -> None:
#     print("Shutting down the application...")